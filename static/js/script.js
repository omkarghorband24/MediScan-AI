const imageInput = document.getElementById("imageInput");

const previewImage = document.getElementById("previewImage");

const removeBtn = document.getElementById("removeBtn");

imageInput.addEventListener("change",function(){

    const file = this.files[0];

    if(file){

        previewImage.src = URL.createObjectURL(file);

        previewImage.style.display="block";

        removeBtn.style.display="inline-block";

    }

});

removeBtn.addEventListener("click",function(){

    imageInput.value="";

    previewImage.src="";

    previewImage.style.display="none";

    removeBtn.style.display="none";

});