    function addLetterToInput(letter) {
        document.getElementById('userWordInput').value += letter;
    }

    let letterClicked = false;

    function handleLetterClick(element, letter) {
        if (!letterClicked) {
            letterClicked = true;
            element.style.opacity = '0.5'; // Changer l'opacité pour griser la lettre
            // Autres actions à effectuer lors du clic sur la lettre
            addLetterToInput(letter);
        }
        else {
            letterClicked = false;
            element.style.opacity = '1';
            document.getElementById('userWordInput').value -= letter;
        }
    }

    function resetLetterBoxes() {
        letterClicked = false;
        const letterBoxes = document.querySelectorAll('.letter-box');
        letterBoxes.forEach(box => {
            box.style.opacity = '1'; // Réinitialiser l'opacité des lettres
        });
    }

    _____________________

        function addLetterToInput(letter) {
        document.getElementById('userWordInput').value += letter;
    }

    function handleLetterClick(element, letter) {
        const isClicked = element.getAttribute('data-clicked') === 'true';

        if (!isClicked) {
            element.setAttribute('data-clicked', 'true');
            element.style.opacity = '0.5'; // Change opacity to visually indicate the clicked state

            // Additional actions when the letter is clicked
            addLetterToInput(letter);
        }

        if (isClicked) {
            const userInput = document.getElementById('userWordInput');
            const userWord = userInput.value;

            element.setAttribute('data-clicked', 'false');
            element.style.opacity = '1';

            // Check if the clicked letter is present in the userWordInput
            if (userWord.includes(letter)) {
                // Remove the letter from the userWordInput value
                const modifiedWord = userWord.replace(letter, '');
                userInput.value = modifiedWord;
            }
        }

    }