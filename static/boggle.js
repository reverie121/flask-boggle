let score = 0
let timer = 6 // FIX THIS AS NEEDED WHEN READY (set to 60)

function timerColorChange(timer) {
    if (timer == 49) {
        $('#timer').css("color","rgb(195,195,0)");
    }
    else if (timer == 29) {
        $('#timer').css("color","orange");
    }
    else if (timer == 9) {
        $('#timer').css("color","red");
    }
}

async function startTimer() {
    $('#timer').text(`${timer}`);
    let inter = setInterval(async function() {
        if (timer > 1) {
            timer -= 1;
            timerColorChange(timer);
            $('#timer').text(`${timer}`);
        }
        else {
            $('#timer').text(`0`);
            clearInterval(inter);
            return await axios.post('/end-game', {score: score})

        }
    }, 100); // FIX THIS AS NEEDED WHEN READY (set to 1000)
}

function word_scored_message(responseField, guess) {
    responseField.css({"color": "green", "background-color": "rgba(0,255,0,0.1)"});
    if ($('#guess').val().length > 1) {
        responseField.text(`'${guess.toUpperCase()}' has been scored for ${guess.length} points!`);
    } else {
        responseField.text(`'${guess.toUpperCase()}' has been scored for ${guess.length} point!`);
    }
}

function word_not_scored_message(responseField, guess, response) {
    let msg = '';
    if (response.data == 'word-already-scored') {
        msg = `'${guess.toUpperCase()}' has already been scored!`;
    }
    else if (response.data == 'not-on-board') {
        msg = `'${guess.toUpperCase()}' is not on this board...`;
    }
    else {
        msg = `'${guess.toUpperCase()}' is not a word...`;
    }
    responseField.text(msg).css({"color": "red", "background-color": "rgba(255,0,0,0.1)"})
}

async function submitGuess() {
    let guess = $('#guess').val();
    let responseField = $('#guess-response');
    const response = await axios.get(`/make-guess?guess=${guess}`);
    if (response.data == 'ok') {
        word_scored_message(responseField, guess);
    } else {
        word_not_scored_message(responseField, guess, response);
    }
    return response.data
}

function adjust_score(){
    const points = $('#guess').val().length;
    score += points;

    if (score > $('#high_score').text()) {
        $('#high_score').text(`${score}`).css("color", "green");
        $('#score-display').text(`${score}`).css("color", "green");
    }
    else {
        $('#score-display').text(`${score}`);
    }
}

$('#guess-form').submit(async function(e){
    e.preventDefault();
    const response = await submitGuess();
    if (response == 'ok') {
        adjust_score()
    }
    $('#guess').val(''); // empties text input for word scoring
});

startTimer();