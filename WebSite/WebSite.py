from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/user/<user>', methods=['GET', 'POST'])
def hello_world(user):
    if request.method == 'POST':
        #add post
        #include name,
        #location
        #description
        return "hello"
    else:
        #get events near user
        return render_template('index.html',user=user)

@app.route('/event/<event_id>', methods=['GET', 'POST'])
def get_event(event_id):
    if request.method == 'POST':
        #add comment to event
        return 'hella'
    else:
        return render_template('event_chat.html',event_id=event_id)


if __name__ == '__main__':
    app.run(debug="true")
