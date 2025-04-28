import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

import { DockerImageFunction,
        DockerImageCode,
        FunctionUrlAuthType,
        Architecture, 
        FunctionUrl,
      } from 'aws-cdk-lib/aws-lambda';

import { AttributeType,
        BillingMode, 
        Table
 } from 'aws-cdk-lib/aws-dynamodb';
import { platform } from 'os';

export class RagCdkInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    // Create DynamoDB table
    const ragQueryTable = new Table(this, "RagQueryTable", {
      partitionKey: {name:"query_id", type: AttributeType.STRING},
      billingMode: BillingMode.PAY_PER_REQUEST,
    });


    // Lambda fuction for worker
    const workerImageCode = DockerImageCode.fromImageAsset("../image", {
      cmd: ["app_work_handler.handler"],
      buildArgs: {
        platform: "linux/amd64",
      }
    });

    const workerFunction = new DockerImageFunction(this, "RagWorkerFuction", {
      code: workerImageCode, 
      memorySize: 512, 
      timeout: cdk.Duration.seconds(120),
      architecture: Architecture.X86_64,
      environment: {
        TABLE_NAME: ragQueryTable.tableName,
      }
    });


    // Lambda fuction for api
    const apiImageCode = DockerImageCode.fromImageAsset("../image", {
      cmd: ["app_api_handler.handler"],
      buildArgs: {
        platform: "linux/amd64",
      }
    });

    const apiFunction = new DockerImageFunction(this, "RagApiFunction", {
      code: apiImageCode, 
      memorySize: 512, 
      timeout: cdk.Duration.seconds(60),
      architecture: Architecture.X86_64,
      environment: {
        TABLE_NAME: ragQueryTable.tableName,
        WORKER_LAMBDA_NAME: workerFunction.functionName,
      }
    });


    // Create URL AuthType
    const functionURL = apiFunction.addFunctionUrl({
      authType: FunctionUrlAuthType.NONE,
    });


    // Grant permission
    ragQueryTable.grantReadWriteData(workerFunction);
    ragQueryTable.grantReadWriteData(apiFunction);
    workerFunction.grantInvoke(apiFunction);


    // Output URL
    new cdk.CfnOutput(this, "FunctionURL", {
      value: functionURL.url,
    });
    
  }
}
