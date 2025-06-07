from sentence_transformers import SentenceTransformer, util
from query_rag import query_rag

test_data = [
    {
        "query": "What is the main difference between CNNs and RNNs?",
        "expected_answer": "CNNs are mainly used for spatial data like images, while RNNs are designed for sequential data like time series or text."
    },
    {
        "query": "What activation function is commonly used in hidden layers?",
        "expected_answer": "ReLU (Rectified Linear Unit) is one of the most commonly used activation functions in hidden layers."
    },
    {
        "query": "Why is dropout used during training?",
        "expected_answer": "Dropout is used to prevent overfitting by randomly deactivating some neurons during training."
    },
    {
        "query": "How does backpropagation work?",
        "expected_answer": "Backpropagation calculates the gradient of the loss function with respect to each weight using the chain rule, and updates the weights using gradient descent."
    },
    {
        "query": "What is the purpose of a learning rate in training a neural network?",
        "expected_answer": "The learning rate controls how much the model’s weights are updated during training; a rate too high can overshoot minima, while too low can slow convergence."
    },
    {
        "query": "What is the vanishing gradient problem?",
        "expected_answer": "The vanishing gradient problem occurs when gradients become too small during backpropagation, making it hard for the network to learn long-range dependencies."
    },
    {
        "query": "What kind of data is a convolutional neural network (CNN) best suited for?",
        "expected_answer": "CNNs are best suited for image data and other types of spatial data."
    },
    {
        "query": "What is the purpose of using batch normalization?",
        "expected_answer": "Batch normalization helps speed up training and provides some regularization by normalizing the input of each layer."
    },
    {
        "query": "What is the difference between overfitting and underfitting?",
        "expected_answer": "Overfitting means the model performs well on training data but poorly on test data, while underfitting means the model fails to learn the underlying pattern in the training data."
    },
    {
        "query": "Why is GPU acceleration important for training deep learning models?",
        "expected_answer": "GPU acceleration significantly speeds up the training process by performing parallel computations efficiently, especially for large-scale matrix operations."
    }
]

for item in test_data:
    response = query_rag([], item["query"])
    item["generated_answer"] = response.response_text


model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

for item in test_data:
    emb_expected = model.encode(item["expected_answer"], convert_to_tensor=True)
    emb_generated = model.encode(item["generated_answer"], convert_to_tensor=True)

    similarity = util.cos_sim(emb_expected, emb_generated).item()
    item["cosine_similarity"] = similarity

similarities = [item["cosine_similarity"] for item in test_data]
avg_score = sum(similarities) / len(similarities)
print("Average similarity score:", avg_score)
