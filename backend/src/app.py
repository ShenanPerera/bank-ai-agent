# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import agent  # This is your current AI agent code

# app = Flask(__name__)
# CORS(app)  # Allow requests from React

# @app.route("/query", methods=["POST"])
# def query_agent():
#     data = request.json
#     user_query = data.get("query", "")
#     response = agent.answer_or_escalate(user_query)
#     return jsonify({"response": response})

# @app.route("/analytics", methods=["GET"])
# def analytics():
#     agent.show_analytics()
#     return jsonify({"message": "Analytics shown in backend console"})

# if __name__ == "__main__":
#     app.run(debug=True)
