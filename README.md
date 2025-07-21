👤 Facial Recognition-Based Employee Authentication

A cloud-based facial recognition system that authenticates employees using Amazon Rekognition and retrieves employee details from AWS DynamoDB. Built using Python and AWS SDK (Boto3), this serverless architecture is scalable, secure, and efficient for modern employee verification systems.

 🚀 Features

- 📸 Face detection and recognition using Rekognition
- 🔐 Authentication against stored employee data in DynamoDB
- ☁️ Serverless design using AWS services
- 🛡️ IAM-based access control
- 📦 Easy deployment using AWS Lambda (optional)

## 🛠️ Tech Stack

| Technology      | Purpose                       |
|-----------------|-------------------------------|
| Python          | Core programming language     |
| AWS Rekognition | Face indexing & matching      |
| AWS DynamoDB    | Storing employee information  |
| Boto3           | AWS SDK for Python            |
| IAM             | Role-based access management  |

## 📂 Project Structure

facial-authentication-aws/
│
├── register_face.py # Index face to Rekognition collection
├── recognize_face.py # Match face against collection
├── authenticate_employee.py # Lookup employee data in DynamoDB
├── README.md # Project documentation
└── .gitignore # Git ignored files

🧑‍💻 How It Works

1. **Face Registration:**
   - Upload an image of an employee.
   - Rekognition indexes the face into a collection.
   - The `FaceId` is saved as the `EmployeeID` in DynamoDB with employee details.

2. **Authentication:**
   - Capture or upload a new image for login.
   - Rekognition compares the face with stored collection.
   - If a match is found, the `FaceId` is used to fetch employee data from DynamoDB.

✅ Setup Instructions

🔹 Prerequisites

- Python 3.x
- AWS CLI configured (`aws configure`)
- IAM user with Rekognition and DynamoDB permissions

🔹 Install dependencies

```bash
pip install boto3
