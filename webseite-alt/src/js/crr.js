// Warte, bis das DOM vollständig geladen ist
document.addEventListener("DOMContentLoaded", function () {
  
  // Wähle alle Überschriften mit der Klasse "dropdown-trigger" aus
  var dropdownTriggers = document.querySelectorAll(".dropdown-trigger");

  // Schleife durch alle Dropdown-Überschriften
  for (var i = 0; i < dropdownTriggers.length; i++) {
    
	// Füge einen Hover-Eventlistener zu jeder Dropdown-Überschrift hinzu
    dropdownTriggers[i].addEventListener("mouseenter", function () {
      // Finde das nächste Geschwister-Element (die Dropdown-Inhalte)
      var dropdownContent = this.nextElementSibling;
		
      // Zeige das Dropdown
      dropdownContent.style.display = "block";
	  // Füge die Klasse dem H2 Element (hier this) hinzu open hinzu, sodass aus dem + ein - wird
	  this.classList.add("open");
    });

    // Füge einen Hover-Eventlistener zum Schließen des Dropdowns hinzu
    dropdownTriggers[i].addEventListener("mouseleave", function () {
      // Finde das nächste Geschwister-Element (die Dropdown-Inhalte)
      var dropdownContent = this.nextElementSibling;

      // Verstecke das Dropdown
      dropdownContent.style.display = "none";
	  // Entferne die Klasse open vom H2 Element (hier this), sodass aus dem angezeigten - wieder ein + wird
	  this.classList.remove("open");
    });
  }
});
