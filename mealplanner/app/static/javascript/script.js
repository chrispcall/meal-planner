///////////////////////////////Begin Show 'Add Meal' form///////////////////////////////
var add_meal = document.getElementsByClassName('box')[0];
var date_elements = document.getElementsByClassName('date');
var close = document.getElementsByClassName('close')[0];
var i;

for (i = 0; i < date_elements.length; i++) {
    date_elements[i].addEventListener("click", function (event) {
        
        var _date_just_clicked_ = event.target.innerHTML;
        //Loads the date string into the form text box (even if it's not currently in the db we want to show it)
        date_box.textContent = _date_just_clicked_;
        //Uses the date string from the date_element that was just clicked to retrieve data from db
        getDataFromDb(_date_just_clicked_);
        //Show the hidden form
        fadeIn();
    
    });
}

close.addEventListener("click", function (event) {
    fadeOut();
});

function fadeOut() {
    add_meal.classList.remove('fadeIn');
    add_meal.classList.add('fadeOut');
 }
 function fadeIn() {
    add_meal.classList.remove('fadeOut');
    add_meal.classList.remove('starting');
    add_meal.classList.add('fadeIn');
 }
//End Show 'Add Meal' form



/////////////////Begin getting JSON data from db where the date value = clicked element/////////////////////
//Get all input objects from the 'add_meal' form:
var date_box = document.getElementsByClassName('date_label')[0];
var title_box = document.querySelector("#title");
var url_box = document.querySelector("#url");
var ingredients_box = document.querySelector("#ingredients");
var notes_box = document.querySelector("#notes");
 
//Takes a date and loads all of the retrieved data onto the 'add_meal' form
function getDataFromDb(_date_) {
 
$.ajax({
    type: 'GET',
    dataType: 'json',
    url: ('/get_values/' + _date_),
    success: function(response){
        date_box.value = response.date;
        title_box.value = response.title;
        url_box.value = response.url;
        ingredients_box.value = response.ingredients;
        notes_box.value = response.notes;
    },
    error: function(data) {
    }
});
highlightProteins();
}
//End getting JSON data from db where the date value = clicked element

  
//////////////////////////////Begin Highlighting Protein Names//////////////////////////////
var list_of_proteins = ['abalone','american bison','anchovies','anchovy','antelope','back bacon','bacon','barbary sheep','basa','bass','beef','beef jerky','bighorn sheep','bison','bratwurst','brat','buffalo','bushpig','camel','canadian bacon','canadian-style bacon','canned chicken','capybara','caraba','caribou (reindeer)','carp','catfish','cattle','chicken','chicken breast','chicken drumstick','chicken drumsticks','chicken thigh','chicken wing','chorizo','clam','clams','cod','conch','corned beef','cornish hen','crab','crappie','crayfish','cuttlefish','dall sheep','deer','domestic goat','domestic pig','domestic sheep','dove','duck','eared seal','earless seal','emu','escargots','eye of round steak','fish','flounder','goose','ground beef','ground pork','ground turkey','groundhog','grouper','grouse','guinea fowl','guinea pig','haddock','halbut','halibut','ham','hamburger','hare','herring','ibex','javelina','kangaro','kingfish','lamb','light tuna','llama','lobster','loc','mackerel','mahi mahi','mahi-mahi','marlin','moose','mountain goat','mussel','new world quail','octopus','opossum','orange roughy','ostrich','oyster','partridge','peccary','pepperoni','perch','pheasant','pigeon','pika','pike','pollock','pork chop','pork chops','pork loin','pork tenderloin','pork','pot roast','prawn','quail','rabbit','red river hog','roast','roast beef','roasted turkey breast','salmon','sardine','sardines','scallop','scallops','shrimp','snail','snapper','sockeye salmon','sole','steak','swordfish','tilapia','tofu','trout','tuna','tuna fish','turkey','turkey breast','veal','venison','wallaby','walleye','walrus','wild boar','wild goat','yak','yellowfin tuna'];

function highlightProteins() {
els = document.getElementsByClassName('ingredient');

Array.prototype.forEach.call(els, function(el) {
 
    new_content = el.textContent;
 
    for (i in list_of_proteins) {
        if (new_content.toLowerCase().includes(list_of_proteins[i])){
            var regex = new RegExp(list_of_proteins[i], 'gi')
        new_content = new_content.replace(regex, '<span style="background:rgba(255,0,0,.3);box-shadow: 2px 0 0 rgba(255,0,0,.3), -2px 0 0 rgba(255,0,0,.3)">' + list_of_proteins[i] + '</span>');
         }
      }
    el.innerHTML = new_content;
});
}
highlightProteins();
//End Highlighting Protein Names


var go_back = document.getElementsByClassName('backward')[0];
go_back.addEventListener("click", function (event) {
var url = window.location.pathname;
window.location.href = url.split("/")[0] + "/week/" + (parseInt(url.split("/")[2])-1);
});

var go_back = document.getElementsByClassName('forward')[0];
go_back.addEventListener("click", function (event) {
var url = window.location.pathname;
window.location.href = url.split("/")[0] + "/week/" + (parseInt(url.split("/")[2])+1);
});

