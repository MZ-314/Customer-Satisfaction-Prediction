
# 🚀 DEPLOYMENT GUIDE - Customer Satisfaction Predictor

## 📦 Files Needed for Deployment:
- app.py
- random_forest_model.pkl
- logistic_regression_model.pkl
- scaler.pkl
- label_encoders.pkl
- requirements.txt

---

## 🌐 DEPLOYMENT OPTIONS:

### Option 1: Streamlit Cloud (FREE & EASIEST)

1. **Create a GitHub Repository:**
   - Go to github.com and create a new repository
   - Upload all 6 files listed above

2. **Deploy on Streamlit Cloud:**
   - Go to share.streamlit.io
   - Click "New app"
   - Connect your GitHub account
   - Select your repository
   - Select app.py as the main file
   - Click "Deploy"
   
3. **Done!** Your app will be live in minutes with a public URL

---

### Option 2: Heroku

1. **Additional Files Needed:**
   - Create Procfile with content: `web: streamlit run app.py --server.port=$PORT`
   - Create setup.sh with Streamlit config

2. **Deploy:**
   - Install Heroku CLI
   - Run: `heroku login`
   - Run: `heroku create your-app-name`
   - Run: `git push heroku main`

---

### Option 3: Local Network Deployment

1. **Run on Your Computer:**
```bash
   pip install -r requirements.txt
   streamlit run app.py
```

2. **Access from Other Devices:**
   - The app will show a Network URL (e.g., http://192.168.1.x:8501)
   - Other devices on the same network can access this URL

---

### Option 4: Google Cloud Platform / AWS / Azure

1. **Use Docker Container:**
   - Create a Dockerfile
   - Build and push to container registry
   - Deploy on Cloud Run / ECS / App Service

2. **Or use VM Instance:**
   - Create a VM
   - Install Python and dependencies
   - Run streamlit app
   - Configure firewall rules

---

## 🔧 TESTING LOCALLY FIRST:

Before deployment, test locally:
```bash
# Navigate to your folder
cd path/to/your/folder

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at http://localhost:8501

---

## 💡 TIPS:

✓ **Streamlit Cloud is recommended** for beginners (free, easy, fast)
✓ Make sure all .pkl files are in the same directory as app.py
✓ Check that file paths in app.py match your structure
✓ Test locally before deploying to catch any issues
✓ Use environment variables for sensitive data
✓ Monitor your app's performance after deployment

---

## 🆘 TROUBLESHOOTING:

**Issue:** Model files not found
**Solution:** Ensure all .pkl files are in the same directory as app.py

**Issue:** Module not found error
**Solution:** Check requirements.txt includes all necessary packages

**Issue:** Encoding error
**Solution:** Verify input values match the training data categories

---

## 📊 RECOMMENDED: Streamlit Cloud Deployment Steps

1. Create GitHub account (if you don't have one)
2. Create new repository named "customer-satisfaction-predictor"
3. Upload all 6 files to the repository
4. Go to share.streamlit.io
5. Sign in with GitHub
6. Click "New app"
7. Select your repository and app.py
8. Click "Deploy"
9. Wait 2-3 minutes
10. Share your public URL! 🎉

Your app will be accessible at: https://your-app-name.streamlit.app

---

**Need help?** Check Streamlit documentation: https://docs.streamlit.io/
