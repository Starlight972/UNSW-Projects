// UITest.spec.js created with Cypress
//
// Start writing your Cypress tests below!
// If you're unfamiliar with how Cypress works,
// check out the link below and learn how to write your first test:
// https://on.cypress.io/writing-first-test
context('UI Test', () => {

	beforeEach('should enter register page', () => {
		cy.visit('localhost:3000');
		cy.wait(2000);
		cy.get('button[id=register]').click();
		// cy.get('button[id=login]').click();

		// check that it should in register page now
		cy.url().should('eq', 'http://localhost:3000/register');
		//cy.url().should('eq', 'http://localhost:3000/login'); 
	});

	it('Happy Path', () => {
		
		/*****************************************/
		/********* Register Successfully *********/
		/*****************************************/

		// check that it should in register page now
		cy.url().should('eq', 'http://localhost:3000/register'); 

		// Register with the correct credentials
		const email = 'hayden@email.com';
		const name = 'Hayden';
		const password = 'hayden';
		const confirmPassword = 'hayden';

		cy.get('input[id=registerEmail]').focus().type(email);
		cy.get('input[id=registerName]').focus().type(name);
		cy.get('input[id=registerPassword]').focus().type(password);
		cy.get('input[id=registerPassword2]').focus().type(confirmPassword);
		cy.wait(2000);
		cy.get('button').click();


		/*****************************************/
		/**** Create A new Game Successfully *****/
		/*****************************************/

		// Check that it is successful enter into Dashboard
		cy.url().should('eq', 'http://localhost:3000/dashboard');

		cy.get('button[id=addQuiz]').click();
		const quizName = 'First Quiz';
		cy.get('input[id=outlined-basic]').focus().type(quizName);
		cy.wait(2000);
		cy.get('button[id=createQuiz]').click();

		/*****************************************/
		/****** Start the Game Successfully ******/
		/*****************************************/

		// Check that it is still in Dashboard
		cy.url().should('eq', 'http://localhost:3000/dashboard');

		cy.wait(2000);
		cy.get('button[id=startGame]').click();

		// check that session ID shows successfully
		cy.get('button[id=session]').contains('Session ID:');

		/*****************************************/
		/******* End the Game Successfully *******/
		/*****************************************/

		// Check that it is still in Dashboard
		cy.url().should('eq', 'http://localhost:3000/dashboard');

		cy.wait(2000);
		cy.get('button[id=endGame]').click();

		// check that show result confirm box popup successfully
		cy.get('h1').contains('Would you like to view the results?');

		/*****************************************/
		/*** Load the result page successfully ***/
		/*****************************************/

		cy.wait(2000);
		cy.get('button[id=showResults]').click();

		/*****************************************/
		/********** Logout successfully **********/
		/*****************************************/

		cy.wait(2000);
		cy.get('div[id=backToDashboard]').click();

		// Check that it is in Dashboard
		cy.url().should('eq', 'http://localhost:3000/dashboard');

		cy.wait(2000);
		cy.get('p[id=logout]').click();

		// check that logout successfully and enter into login page
		cy.get('h1[id=loginTitle]').contains('Log In');

		/*****************************************/
		/********* Log back successfully *********/
		/*****************************************/

		// Check that it is in login page
		cy.url().should('eq', 'http://localhost:3000/login');

		// Login with the correct credentials
		cy.get('input[id=logInEmail]').focus().type(email);
		cy.get('input[id=logInPassword]').focus().type(password);
		cy.wait(2000);
		cy.get('button').click();
	});

	it('Path for checking edit game', () => {
		
		/*****************************************/
		/********* Register Successfully *********/
		/*****************************************/

		// check that it should in register page now
		cy.url().should('eq', 'http://localhost:3000/register'); 

		// Register with the correct credentials
		const email = 'hayden@example.com';
		const name = 'Hayden';
		const password = 'hayden';
		const confirmPassword = 'hayden';

		cy.get('input[id=registerEmail]').focus().type(email);
		cy.get('input[id=registerName]').focus().type(name);
		cy.get('input[id=registerPassword]').focus().type(password);
		cy.get('input[id=registerPassword2]').focus().type(confirmPassword);
		cy.wait(2000);
		cy.get('button').click();


		/*****************************************/
		/**** Create A new Game Successfully *****/
		/*****************************************/

		// Check that it is successful enter into Dashboard
		cy.url().should('eq', 'http://localhost:3000/dashboard');

		cy.get('button[id=addQuiz]').click();
		const quizName = 'First Quiz';
		cy.get('input[id=outlined-basic]').focus().type(quizName);
		cy.wait(2000);
		cy.get('button[id=createQuiz]').click();

		/*****************************************/
		/**** Load GameEidt Page Successfully ****/
		/*****************************************/

		// Check that it is still in Dashboard
		cy.url().should('eq', 'http://localhost:3000/dashboard');

		cy.wait(2000);
		cy.get('button[id=editGame]').click();

		// check that game name shows successfully
		cy.get('h1[id=gameName]').contains('First Quiz');

		/*****************************************/
		/***** Create Question Successfully ******/
		/*****************************************/

		cy.get('button[id=createQuestion]').click();

		const questionText = 'The first question';
		cy.get('input[id=questionText]').focus().type(questionText);
		cy.wait(2000);
		cy.get('button[id=saveBtn]').click();

		// check that show question content confirm box popup successfully
		cy.get('span[id=questionContent]').contains(questionText);

		/*****************************************/
		/********** Logout successfully **********/
		/*****************************************/

		cy.wait(2000);
		cy.get('p[id=logout]').click();

		// check that logout successfully and enter into login page
		cy.get('h1[id=loginTitle]').contains('Log In');

		/*****************************************/
		/********* Log back successfully *********/
		/*****************************************/

		// Check that it is in login page
		cy.url().should('eq', 'http://localhost:3000/login');

		// Login with the correct credentials
		cy.get('input[id=logInEmail]').focus().type(email);
		cy.get('input[id=logInPassword]').focus().type(password);
		cy.wait(2000);
		cy.get('button').click();

		// Check that it is in Dashboard page successfully
		cy.url().should('eq', 'http://localhost:3000/dashboard');
	});
});
