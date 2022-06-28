var field_clear_button = document.getElementById("field_clear_button");
field_clear_button.addEventListener("click", function(e){
	document.getElementById("character_name").value = "";
	document.getElementById("password").value = "";
});
var input_fields = document.getElementsByClassName('form-control')
for(var i = 0; i < input_fields.length; i++){
    (function(index){
        input_fields[index].addEventListener('input', function() {
            this.classList.remove("invalid-border");
        });
        input_fields[index].addEventListener('focusout', function() {
            if (this.value == "" || this.value == null) {
                this.classList.add("invalid-border");
            }
        })
    })(i);
}