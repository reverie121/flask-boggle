class Boggle {
    constructor() {
        this.score = 0
        this.timer = 60 // FIX THIS AS NEEDED WHEN READY (set to 60)
    }

    timerColorChange() {
        if (this.timer == 49) {
            $('#timer').css("color","rgb(195,195,0)");
        }
        else if (this.timer == 29) {
            $('#timer').css("color","orange");
        }
        else if (this.timer <= 9) {
            $('#timer').css("color","red");
        }
    }

    async start_timer() {
        $('#timer').text(`${this.timer}`);
        let inter = setInterval(async => {
            this.timer -= 1;
            this.timerColorChange();
            $('#timer').text(`${this.timer}`);
            if (this.timer == 0) {
                clearInterval(inter);
                $('#form-container').hide();
                $('#new-game-button-container').show();
                let gp = parseInt($('#games-played').text()) + 1;
                $('#games-played').text(gp);
                $('#score').val(this.score);
            }
        }, 1000);
    }

    word_scored_message(responseField, guess) {
        responseField.css({"color": "green", "background-color": "rgba(0,255,0,0.1)"});
        if ($('#guess').val().length > 1) {
            responseField.text(`'${guess.toUpperCase()}' has been scored for ${guess.length} points!`);
        } else {
            responseField.text(`'${guess.toUpperCase()}' has been scored for ${guess.length} point!`);
        }
    }
    
    word_not_scored_message(responseField, guess, response) {
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
    
    async submitGuess() {
        let guess = $('#guess').val();
        let responseField = $('#guess-response');
        const response = await axios.get(`/make-guess?guess=${guess}`);
        if (response.data == 'ok') {
            this.word_scored_message(responseField, guess);
        } else {
            this.word_not_scored_message(responseField, guess, response);
        }
        return response.data
    }
    
    adjust_score(){
        const points = $('#guess').val().length;
        this.score += points;
        if (score > parseInt($('#high-score').text())) {
            $('#high-score').text(`${this.score}`).css("color", "green");
            $('#score-display').text(`${this.score}`).css("color", "green");
        }
        else {
            $('#score-display').text(`${this.score}`);
        }
    }
}

function on_page_load() {
    $('#new-game-button-container').hide();
    $('#form-container').show();

    const boggle = new Boggle();
    boggle.start_timer();

    $('#form-container').on('submit', 'form', async function(e){
        e.preventDefault();
        const response = await boggle.submitGuess();
        if (response == 'ok') {
            boggle.adjust_score()
        }
        $('#guess').val(''); // empties text input for word scoring
    });
}

document.onload = on_page_load();