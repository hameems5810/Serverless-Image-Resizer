# Serverless Image Resizer
**Automatically resize uploaded images using AWS Lambda and S3.**

Large, unoptimized images slow down websites and waste storage—but manually resizing before every upload is tedious and error-prone. This project builds a simple **event-driven, serverless pipeline**: when a user uploads a JPEG to an **S3 input bucket**, an **AWS Lambda** function automatically resizes it (max width **300px**, aspect ratio preserved) and saves the processed copy to an **S3 output bucket**.


---

## What it does
- Upload an image to **`hameem-image-input`**
- S3 triggers **`hameem-image-resizer`** (Lambda)
- Lambda resizes the image using **Pillow** (via **Lambda Layer**)
- Lambda writes the result to **`hameem-image-output`** as:  
  `resized-<original_filename>.jpg`
- Execution logs + metrics are captured in **CloudWatch**

---

## Architecture Diagram
**Flow:**  
User → S3 (**input**) → S3 ObjectCreated event → Lambda (**resizer + Pillow layer**) → S3 (**output**) → CloudWatch (logs/metrics)

**Core components**
- **AWS Lambda (Python 3.12):** compute that runs only when uploads happen
- **Amazon S3:** durable storage + native event trigger
- **IAM Role (`lambda-s3-readonly-role`):** permissions for S3 + CloudWatch
- **CloudWatch:** logs and metrics (Invocations, Duration, Errors, etc.)
- **Lambda Layer (Klayers Pillow):** image processing library inside Lambda

---

## Tech Stack
- **Compute:** AWS Lambda (Python 3.12)
- **Storage/Event Source:** Amazon S3 (2 buckets)
- **Security:** IAM Roles/Policies
- **Observability:** CloudWatch Logs + Metrics
- **Dependency:** Pillow via Lambda Layer (Klayers)

---

## Setup (AWS Console Only)
1. **Create two S3 buckets** (region: `us-east-1`)
   - `hameem-image-input`
   - `hameem-image-output`

2. **Create IAM role**: `lambda-s3-readonly-role`
   - Trusted entity: **Lambda**
   - Permissions:
     - CloudWatch logging permissions
     - S3 permissions to **read from input** and **write to output**
     - *(Lab note: AmazonS3FullAccess was used temporarily to fix AccessDenied during debugging; least-privilege is recommended—see Security section.)*

3. **Create Lambda function**: `hameem-image-resizer`
   - Runtime: **Python 3.12**
   - Execution role: `lambda-s3-readonly-role`
   - Memory: **128 MB**
   - Timeout: **3 seconds**

4. **Attach Pillow Lambda Layer**
   - Add **Klayers Pillow (python3.12)** layer under *Layers*

5. **Set environment variable**
   - `OUTPUT_BUCKET = hameem-image-output`

6. **Add S3 trigger**
   - Source: `hameem-image-input`
   - Event type: **ObjectCreated (PUT)**

7. **Deploy + test**
   - Upload a JPEG into `hameem-image-input`
   - Confirm an output file appears in `hameem-image-output` with `resized-` prefix

---

## Monitoring
- **CloudWatch Logs:** per-invocation step-by-step logs (great for debugging triggers + permissions)
- **CloudWatch Metrics:** Invocations, Duration, Errors, Throttles, ConcurrentExecutions  
  *(Future improvement: add alarms + notifications.)*

---

## Screenshots (README Gallery)

### Deployed Resources

#### 1) S3 Buckets — `hameem-image-input` and `hameem-image-output`
 hameem-image-input
<p align="center">
  <img width="975" height="576" alt="S3 bucket list (view 1)" src="https://github.com/user-attachments/assets/f215746f-480d-481d-addb-e2ca95a9dff5" />
  <br/>
  </p>
      hameem-image-output
  <p align="center">
  <img width="975" height="581" alt="S3 bucket list (view 2)" src="https://github.com/user-attachments/assets/08dd51f7-e5f1-4687-b9b6-3d329fca6f4a" />
</p>

#### 2) Lambda Function Overview — `hameem-image-resizer`
<p align="center">
  <img width="975" height="581" alt="Lambda function overview" src="https://github.com/user-attachments/assets/2f103f63-9812-4136-bc1e-6a56d4ccab9f" />
</p>

#### 3) S3 Trigger Attached to Lambda
<p align="center">
  <img width="975" height="581" alt="S3 trigger attached to Lambda" src="https://github.com/user-attachments/assets/075b5d41-2a22-4b39-9b0f-362875595d2e" />
</p>

#### 4) Environment Variable — `OUTPUT_BUCKET`
<p align="center">
  <img width="975" height="582" alt="Lambda environment variable OUTPUT_BUCKET" src="https://github.com/user-attachments/assets/da44ec99-9b6d-4f76-bb61-3a355970b119" />
</p>

#### 5) Lambda General Configuration — Runtime / Memory / Timeout
<p align="center">
  <img width="975" height="582" alt="Lambda general configuration" src="https://github.com/user-attachments/assets/5f634aaf-10de-41c3-b2d1-5e9efc69e807" />
</p>

#### 6) Lambda Code Editor — Resize Logic
<p align="center">
  <img width="975" height="583" alt="Lambda code editor showing resize logic" src="https://github.com/user-attachments/assets/7d5d7e85-8a1c-4daf-a144-3ffe06956750" />
</p>

#### 7) Lambda Layer — Pillow Attached
<p align="center">
  <img width="975" height="579" alt="Lambda layer with Pillow attached" src="https://github.com/user-attachments/assets/75662877-2557-4536-98d0-0064c3b64cf4" />
</p>

#### 8) IAM Execution Role Permissions — `lambda-s3-readonly-role`
<p align="center">
  <img width="975" height="556" alt="IAM execution role permissions" src="https://github.com/user-attachments/assets/f6e15077-92dc-4b92-aae2-e53a10fad7a7" />
</p>

#### 9) IAM Role with S3 Full Access (Lab / Debug Step)
<p align="center">
  <img width="975" height="556" alt="IAM role with S3 Full Access (debug)" src="https://github.com/user-attachments/assets/a27238e8-6c20-4e94-9f34-e3411b9ccc11" />
</p>

#### 10) Input Bucket After Upload — `hameem-image-input`
<p align="center">
  <img width="975" height="581" alt="Input bucket after upload" src="https://github.com/user-attachments/assets/c331bdd1-3ada-4c4e-b01a-151e0362430f" />
</p>

#### 11) Output Bucket After Processing — `hameem-image-output`
<p align="center">
  <img width="975" height="579" alt="Output bucket after processing" src="https://github.com/user-attachments/assets/2f285f3e-3a12-4ee4-a085-8a889feec27e" />
</p>

---

### Monitoring

#### 12) CloudWatch Metrics — Invocations / Duration / Errors
<p align="center">
  <img width="975" height="581" alt="CloudWatch metrics for Lambda" src="https://github.com/user-attachments/assets/3525c4ce-e021-477e-9ec1-4258c36eb28b" />
</p>

#### 13) CloudWatch Logs — S3-Triggered Invocation Output
<p align="center">
  <img width="975" height="578" alt="CloudWatch log stream showing S3-triggered run" src="https://github.com/user-attachments/assets/6bc56332-2613-43c6-ae76-be4706a6bc07" />
</p>
