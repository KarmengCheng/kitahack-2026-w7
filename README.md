# KitaHack 2026: Go Live! Cloud Deployment with Cloud Run and Firebase

Welcome to the KitaHack 2026 workshop! In this hands-on session, you'll build and deploy a full-stack serverless application using Google Cloud Run and Firebase Hosting.

## What You'll Build

- **Backend ("The Brain")**: A Python Flask API deployed on Google Cloud Run
- **Frontend ("The Face")**: A web interface hosted on Firebase that talks to your backend

---

## 📍 Checkpoint 0: The Cloud Foundation (After Google Cloud Credit is claimed)

### Phase A: Set up on Google Cloud Console

1. **Open Google Cloud Console**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)

2. **Create Your Project**
   - Click the dropdown at the top left
   - Click **New Project**
   - Name it: `kitahack-2026-yourname` (use something unique)
   - Click **Create**
   - Wait 10 seconds for it to finish loading

3. **Link Your Billing Account (The "Free Money" Step)**
   - Go to the left-hand menu → **Billing**
   - Click **Link a Billing Account**
   - Select the billing account with your $5 Google Cloud student credit
   - Verify your credit: Check the **Credits** tab to see your $5 active

### Phase B: The Terminal Handshake

Now we'll connect your local terminal to the cloud project you just created.

1. **Check Who Is Logged In**
   ```bash
   gcloud auth list
   ```
   - If your email doesn't have a `*` next to it, run:
   ```bash
   gcloud auth login
   ```

2. **Connect Terminal to Your Project**
   - Replace `YOUR_PROJECT_ID` with your actual project ID, not the project name (e.g., `kitahack-2026-w7-481242`):
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable Required APIs**
   - Run this command to turn on the cloud services:
   ```bash
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
   ```

---

## 📍 Checkpoint 1: The Local Workspace

### Step 1.1: Create the Folders

Open your terminal and run:

```bash
mkdir kitahack-2026
cd kitahack-2026
mkdir backend frontend
```

### Step 1.2: Open in VS Code

Open the entire `kitahack-2026` folder in VS Code:

```bash
code .
```

---

## 📍 Checkpoint 2: Building the "Brain" (The Python API)

### Step 2.1: Write the Requirements

1. Inside the `backend` folder, create a file called `requirements.txt`
2. Paste this content:

```
Flask==3.0.0
gunicorn==21.2.0
flask-cors==4.0.0
```

### Step 2.2: Write the App Code

1. Inside the `backend` folder, create a file called `main.py`
2. Paste this code:

```python
import os
import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS allows your Firebase frontend to talk to this Cloud Run backend safely
CORS(app)

@app.route('/')
def home():
    return "Backend is alive! Go to /api/vibe to check the vibe."

@app.route('/api/vibe', methods=['GET'])
def vibe_check():
    # This simulates our AI or database logic
    vibes = [
        "AI says: You are crushing it! 🚀",
        "AI says: Don't forget to hydrate! 💧",
        "AI says: Deployments are looking green! ✅",
        "AI says: Sleep is for the weak (just kidding, sleep is important) 😴"
    ]
    return jsonify({"message": random.choice(vibes)})

if __name__ == "__main__":
    # Cloud Run injects the PORT environment variable automatically (usually 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
```

### Step 2.3: The Magic Deployment Command

1. Open your terminal and navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Run the deployment command:
   ```bash
   gcloud run deploy kitahack-api --source . --region us-central1 --allow-unauthenticated
   ```

3. When prompted "Do you want to continue (Y/n)?", type `Y` and press Enter

> **What's happening?**

Google Cloud's Buildpacks are analyzing your code, detecting it's a Python app, and automatically building a secure, optimized container, no need to write any DockerFile

4. **Save Your Service URL!**
   - When deployment finishes, the terminal will print a Service URL
   - It looks like: `https://kitahack-api-xyz-uc.a.run.app`
   - Click it to verify: You should see "Backend is alive!"
   - Add `/api/vibe` to the URL to see the JSON response

---

## 📍 Checkpoint 3: Building the "Face" (Firebase Hosting)

### Step 3.1: Navigate to the Frontend Folder

```bash
cd ../frontend
```

### Step 3.2: Log in to Firebase

```bash
firebase login
```

- This will open a browser window
- Authenticate with the same Google account you used for your project

### Step 3.3: Create the project in Firebase Console

1. Click **Create a New Firebase Project**

2. Instead of create a new project

Click the **Add Firebase to Google Cloud project** to sync with the backend at below

3. Select the Google Cloud Project created just now (eg. kitahack-2026-yourname)

4. Click continue until it's done

### Step 3.4: Initialize the Project

Run the setup command:

```bash
firebase init hosting
```

**⚠️ IMPORTANT: Answer the prompts carefully:**

- **Please select an option:** Use arrow keys to select `Use an existing project`, press Enter
- **Select a default Firebase project:** Find and select your project (e.g., `kitahack-2026-yourname`)
- **What do you want to use as your public directory?** press Enter to select the default public option
- **Configure as a single-page app?** Type `N` and press Enter
- **Set up automatic builds and deploys with GitHub?** Type `N` and press Enter

### Step 3.4: Write the Frontend Code

1. Firebase created a `public` folder inside your `frontend` folder
2. Open `public/index.html` in VS Code
3. **Delete all the default code** inside it
4. Paste this code:

```html
<!DOCTYPE html>
<html>
<head>
    <title>KitaHack Vibe Check</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            padding: 50px;
            background-color: #f8f9fa;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            max-width: 500px;
            margin: auto;
        }
        button {
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            background-color: #4285F4;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            transition: 0.3s;
        }
        button:hover {
            background-color: #3367d6;
        }
        #result {
            margin-top: 30px;
            font-size: 20px;
            font-weight: bold;
            color: #34A853;
            min-height: 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>☁️ KitaHack 2026 ☁️</h1>
        <p>Deploying AI Serverless Apps with Google Cloud</p>
        <br>
        <button onclick="getVibe()">Check The Vibe</button>
        <div id="result"></div>
    </div>

    <script>
        async function getVibe() {
            // REPLACE THIS WITH YOUR ACTUAL CLOUD RUN URL FROM STEP 2.3
            const backendUrl = "https://YOUR-CLOUD-RUN-URL/api/vibe";
            
            const resultDiv = document.getElementById("result");
            resultDiv.innerText = "Loading AI response...";
            resultDiv.style.color = "#FBBC05";

            try {
                const response = await fetch(backendUrl);
                const data = await response.json();
                resultDiv.innerText = data.message;
                resultDiv.style.color = "#34A853";
            } catch (error) {
                resultDiv.innerText = "Error: Could not connect to the cloud.";
                resultDiv.style.color = "#EA4335";
                console.error(error);
            }
        }
    </script>
</body>
</html>
```

5. **CRITICAL:** On line 47, replace `https://YOUR-CLOUD-RUN-URL/api/vibe` with your actual Cloud Run URL from Step 2.3

### Step 3.5: Deploy to the World!

1. Save the `index.html` file
2. Make sure you're in the `frontend` folder in your terminal
3. Run:
   ```bash
   firebase deploy
   ```

4. **Your App Is Live!**
   - In 5-10 seconds, the terminal will print a Hosting URL
   - It looks like: `https://kitahack-2026-yourname.web.app`
   - Click the URL and test the "Check The Vibe" button!

---

## 📍 Checkpoint 4:

Congratulations! You now have:

- ✅ A Python Flask API running on Google Cloud Run
- ✅ A frontend hosted on Firebase
- ✅ A full-stack serverless application accessible from anywhere in the world

This is exactly how enterprise companies build and deploy modern applications. You just did it in under an hour!

---

## Troubleshooting

### "Permission Denied" or "Billing Not Enabled"
- Make sure you linked your billing account in Checkpoint 0, Phase A, Step 3
- Verify your project ID is correct: `gcloud config get-value project`

