from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey
#from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secre233t"
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def get_home_page():
    """Returns HTML Home Page with the Survey and Instructions"""
    responses.clear() 
    return render_template("home_page.html", survey=satisfaction_survey)



@app.route("/start", methods=['POST'])
def get_survey():
    """Gets Survey Question"""
    return redirect('questions/0')



@app.route('/questions/<int:numQues>')
def get_question(numQues):
    """Display Dynamic HTML For Designated Survey Question"""

    #ensure user stays on track
    if (len(responses) == 0):   # if there is no answers, take them to the home page
        return redirect('/')

    if (len(responses) != numQues):  
        flash("Invalid Question ID")
        return redirect(f"/questions/{len(responses)}")

    #display survey question
    ques = satisfaction_survey.questions[numQues]
    return render_template('question_form.html', ques=ques)



@app.route('/answer', methods=['POST'])
def get_answer():
    """Handle the Survey question response"""
    ans = request.form['answer']
    responses.append(ans)
    if (len(responses) == len(satisfaction_survey.questions)):  # if the length of answers = the amount of questions, they are done
        return redirect("/done")
    else:
        return redirect(f"/questions/{len(responses)}")
    


@app.route('/done')
def get_done_page():
    """Display thank you page"""
    return render_template('all_done.html')
