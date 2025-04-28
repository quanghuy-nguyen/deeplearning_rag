FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install pysqlite3-binary

RUN pip install --no-cache-dir -r requirements.txt --upgrade

EXPOSE 8000

ENV IS_USING_IMAGE_RUNTIME = True

COPY .env ${LAMBDA_TASK_ROOT}/.env
COPY src/all-mpnet-base-v2 ${LAMBDA_TASK_ROOT}/all-mpnet-base-v2
COPY src/* ${LAMBDA_TASK_ROOT}/
COPY src/rag_app ${LAMBDA_TASK_ROOT}/rag_app
COPY src/data/vector_store ${LAMBDA_TASK_ROOT}/data/vector_store

