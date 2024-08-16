<script>
    document.addEventListener('DOMContentLoaded', ()=>{
        let reporttype = document.getElementById('reporttype');
        console.log(""+reporttype.value);
        if(reporttype.value == "add"){
            reportidfield = document.getElementById('reportidfield');
            reportidfield.style.display="none";
        }
    });
</script>