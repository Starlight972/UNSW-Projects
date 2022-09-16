/**
 * z5248104	Xin Sun
 * 2022.03.05	Saturday
 * Assignment1 Task3
 */

/** These JavaScript Code is studied for YouTube 
 * https://www.youtube.com/watch?v=PzSxehu4G78
*/

function showPanel(panelIndex) { 
    var tabButtons=document.querySelectorAll(".tabContainer .buttonContainer button ")
    var tabPanels=document.querySelectorAll(".tabContainer .tabPanel")
    tabButtons.forEach(function(node) {
        node.style.backgroundColor="";
        node.style.color="";
    });
    tabButtons[panelIndex].style.backgroundColor="#fff";
    tabButtons[panelIndex].style.color="#5a5ae6";

    tabPanels.forEach(function(node) {
        node.style.display="none";
    });
    tabPanels[panelIndex].style.display="block";
    tabPanels[panelIndex].style.backgroundColor="#fff";
}

document.addEventListener('default-click', showPanel(0));



