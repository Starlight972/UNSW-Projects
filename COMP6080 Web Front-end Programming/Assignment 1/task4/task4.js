/**
 * z5248104	Xin Sun
 * 2022.03.06	Sunday
 * Assignment1 Task4
 */ 


function checkFirstName() {
    var firstName = document.getElementById('first-name').value;
    if (firstName.length < 3 || firstName.length > 50 || firstName == "") {
        document.getElementById("output").innerHTML="Please input a valid firstname";
    }else {
        document.getElementById("output").innerHTML="";
    }
}

function checkLastName() {
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    if (!firstName == "") {
        if (lastName.length < 3 || lastName.length > 50 || lastName == "") {
            document.getElementById("output").innerHTML="Please input a valid lastname";
        }else {
            document.getElementById("output").innerHTML="";
        }
    } else {
        document.getElementById("output").innerHTML="Please input a valid firstname";
    }
    
}

function calculateAge(dateOfBirth) {
    const currentDate = new Date();
    const birthday = new Date(dateOfBirth);
    let age = currentDate.getFullYear() - birthday.getFullYear();
    if (age != 0) {
        let differMonth=currentDate.getMonth() - birthday.getMonth();
        if (differMonth < 0) {
            age = age - 1;
        } else if (differMonth == 0){
            let differDate=currentDate.getDate() - birthday.getDate();
            if (differDate < 0) {
                age = age - 1;
            } 
        } 
    }

    return age;
}

function checkDateOfBirth() {
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    const datePattern = new RegExp("[0-9]{2}/[0-9]{2}/[0-9]{4}");
    var dateOfBirth = document.getElementById('date-of-birth').value;
    var dateList=dateOfBirth.split("/");
    dateOfBirth = dateList[1] + "/" + dateList[0] + "/" + dateList[2];
    let age = calculateAge(dateOfBirth);
    if (firstName == "") {
        document.getElementById("output").innerHTML="Please input a valid firstname";
    } else {
        if (lastName == "") {
            document.getElementById("output").innerHTML="Please input a valid lastname";
        } else {
            if (!datePattern.test(dateOfBirth) || dateOfBirth=="" || isNaN(Date.parse(dateOfBirth)) || age < 0 || isNaN(age)){
                document.getElementById("output").innerHTML="Please enter a valid date of birth";
            }else {
                document.getElementById("output").innerHTML="";
            }
        }
    }
}

function output() {
    var firstName = document.getElementById('first-name').value;
    var lastName = document.getElementById('last-name').value;
    const datePattern = new RegExp("[0-9]{2}/[0-9]{2}/[0-9]{4}");
    var dateOfBirth = document.getElementById('date-of-birth').value;
    var dateList=dateOfBirth.split('/');
    dateOfBirth = dateList[1] + '/' + dateList[0] + '/' + dateList[2]; 
    var age = calculateAge(dateOfBirth);
    var animal=document.getElementById('animals').value;
    var cities= document.getElementsByName('city');
    var citiesArray = [];
    for (var i = 0; i < cities.length; i++) {
        if (cities[i].checked) {
            citiesArray.push(cities[i].value)
        }
    }
    var output = "";
    if (firstName == "") {
        output="Please input a valid firstname";
    } else {
        if (lastName == "") {
            output="Please input a valid lastname";
        } else {
            if (dateOfBirth=="" || isNaN(Date.parse(dateOfBirth)) || age < 0 || isNaN(age) || !datePattern.test(dateOfBirth)){
                output="Please enter a valid date of birth"; 
            } else {
                if(citiesArray.length == 0) {
                    output = "Hello " + firstName + " " + lastName + ", you are " + age +" years old, your favourite animal is " + animal + ", and you've lived in no cities."
                } else {
                    output = "Hello " + firstName + " " + lastName + ", you are " + age +" years old, your favourite animal is " + animal + ", and you've lived in " + citiesArray +"."
                }
            }
        }
    }
    document.getElementById("output").innerHTML=output;
}

function removeContent() {
    document.getElementById("output").innerHTML="";
}

