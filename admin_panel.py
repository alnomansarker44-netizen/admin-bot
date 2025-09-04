from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# 🔑 তোমার Bot এর Railway URL & Token
BOT_API = "https://your-bot-app.up.railway.app"  # <-- এখানে তোমার Bot এর URL বসাও
BOT_TOKEN = "8208693924:AAG7RSPnqVMPmQyxAbXDLpEPgcARFsqaZtU"            # <-- Bot এ সেট করা secret token

# --- সব ইউজার ফেচ করা ---
def fetch_users():
    r = requests.get(f"{BOT_API}/api/users?token={BOT_TOKEN}")
    if r.status_code == 200:
        return r.json()
    return {}

# --- নির্দিষ্ট ইউজার ফেচ করা ---
def fetch_user(user_id):
    r = requests.get(f"{BOT_API}/api/user/{user_id}?token={BOT_TOKEN}")
    if r.status_code == 200:
        return r.json()
    return None

# --- ব্যালেন্স আপডেট ---
def update_balance(user_id, new_balance):
    r = requests.post(
        f"{BOT_API}/api/update_balance/{user_id}?token={BOT_TOKEN}",
        json={"balance": int(new_balance)}
    )
    return r.status_code == 200


# --- হোমপেজ (ইউজার লিস্ট) ---
@app.route("/")
def index():
    users = fetch_users()
    return render_template("index.html", users=users)


# --- এডিট পেজ ---
@app.route("/edit/<user_id>", methods=["GET", "POST"])
def edit(user_id):
    if request.method == "POST":
        new_balance = request.form.get("balance")
        update_balance(user_id, new_balance)
        return redirect(url_for("index"))
    user = fetch_user(user_id)
    return render_template("edit.html", user_id=user_id, user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

