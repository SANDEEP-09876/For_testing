from flask import Flask, request, render_template_string
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ---------------- LEFT DRIVER ----------------
L_DIR1 = 5
L_PWM1 = 6
L_DIR2 = 13
L_PWM2 = 19

# ---------------- RIGHT DRIVER ----------------
R_DIR1 = 12
R_PWM1 = 16
R_DIR2 = 20
R_PWM2 = 21

pins = [L_DIR1, L_PWM1, L_DIR2, L_PWM2,
        R_DIR1, R_PWM1, R_DIR2, R_PWM2]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

# Setup PWM
pwm_L1 = GPIO.PWM(L_PWM1, 1000)
pwm_L2 = GPIO.PWM(L_PWM2, 1000)
pwm_R1 = GPIO.PWM(R_PWM1, 1000)
pwm_R2 = GPIO.PWM(R_PWM2, 1000)

pwm_L1.start(0)
pwm_L2.start(0)
pwm_R1.start(0)
pwm_R2.start(0)

current_speed = 60

# ---------------- MOTOR FUNCTIONS ----------------

def stop():
    pwm_L1.ChangeDutyCycle(0)
    pwm_L2.ChangeDutyCycle(0)
    pwm_R1.ChangeDutyCycle(0)
    pwm_R2.ChangeDutyCycle(0)

def set_speed(speed):
    global current_speed
    current_speed = speed

def forward():
    GPIO.output(L_DIR1, 1)
    GPIO.output(L_DIR2, 1)
    GPIO.output(R_DIR1, 1)
    GPIO.output(R_DIR2, 1)

    pwm_L1.ChangeDutyCycle(current_speed)
    pwm_L2.ChangeDutyCycle(current_speed)
    pwm_R1.ChangeDutyCycle(current_speed)
    pwm_R2.ChangeDutyCycle(current_speed)

def backward():
    GPIO.output(L_DIR1, 0)
    GPIO.output(L_DIR2, 0)
    GPIO.output(R_DIR1, 0)
    GPIO.output(R_DIR2, 0)

    pwm_L1.ChangeDutyCycle(current_speed)
    pwm_L2.ChangeDutyCycle(current_speed)
    pwm_R1.ChangeDutyCycle(current_speed)
    pwm_R2.ChangeDutyCycle(current_speed)

def left():
    GPIO.output(L_DIR1, 0)
    GPIO.output(L_DIR2, 0)
    GPIO.output(R_DIR1, 1)
    GPIO.output(R_DIR2, 1)

    pwm_L1.ChangeDutyCycle(current_speed)
    pwm_L2.ChangeDutyCycle(current_speed)
    pwm_R1.ChangeDutyCycle(current_speed)
    pwm_R2.ChangeDutyCycle(current_speed)

def right():
    GPIO.output(L_DIR1, 1)
    GPIO.output(L_DIR2, 1)
    GPIO.output(R_DIR1, 0)
    GPIO.output(R_DIR2, 0)

    pwm_L1.ChangeDutyCycle(current_speed)
    pwm_L2.ChangeDutyCycle(current_speed)
    pwm_R1.ChangeDutyCycle(current_speed)
    pwm_R2.ChangeDutyCycle(current_speed)

# ---------------- WEB PAGE ----------------

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {background:#111;color:white;text-align:center;}
button {width:90px;height:60px;font-size:20px;margin:5px;}
.slider {width:80%;}
</style>
</head>
<body>

<h2>Speed</h2>
<input type="range" min="0" max="100" value="60" id="speed" class="slider">

<h2>Wheel Control</h2>
<button onmousedown="move('forward')" onmouseup="move('stop')" 
        ontouchstart="move('forward')" ontouchend="move('stop')">↑</button><br>

<button onmousedown="move('left')" onmouseup="move('stop')" 
        ontouchstart="move('left')" ontouchend="move('stop')">←</button>

<button onclick="move('stop')">■</button>

<button onmousedown="move('right')" onmouseup="move('stop')" 
        ontouchstart="move('right')" ontouchend="move('stop')">→</button><br>

<button onmousedown="move('backward')" onmouseup="move('stop')" 
        ontouchstart="move('backward')" ontouchend="move('stop')">↓</button>

<script>
let speedSlider = document.getElementById("speed");

speedSlider.oninput = function(){
fetch('/speed',{
method:'POST',
headers:{'Content-Type':'application/x-www-form-urlencoded'},
body:'speed='+speedSlider.value
});
}

function move(dir){
fetch('/move',{
method:'POST',
headers:{'Content-Type':'application/x-www-form-urlencoded'},
body:'direction='+dir
});
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/move', methods=['POST'])
def move_route():
    direction = request.form['direction']
    if direction == "forward": forward()
    elif direction == "backward": backward()
    elif direction == "left": left()
    elif direction == "right": right()
    elif direction == "stop": stop()
    return ('',204)

@app.route('/speed', methods=['POST'])
def speed_route():
    set_speed(int(request.form['speed']))
    return ('',204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
