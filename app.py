from flask import Flask, render_template, request, jsonify
import aiml
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
	message = request.form['messageText'].encode('utf-8').strip()

	kernel = aiml.Kernel()

	if os.path.isfile("Model/model.brn"):
	    kernel.bootstrap(brainFile = "Model/model.brn")
	else:
	    kernel.bootstrap(learnFiles = os.path.abspath("AIML_Files/startup.xml"), commands = "load aiml")
	    kernel.saveBrain("Model/model.brn")

	# kernel now ready for use
	while True:
	    if message == "quit":
	        exit()
	    elif message == "save":
	        kernel.saveBrain("Model/model.brn")
	    else:
	        bot_response = kernel.respond(message)
	        # print bot_response
	        return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
