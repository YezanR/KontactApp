function verifform()
{
    if( $('#firstName').html() == "")
    {
       alert("Veuillez entrer votre adresse électronique!");
       $('#firstName').focus();
       return false;
    }

    function validateEmail(email)
    {
         var re = /\S+@\S+\.\S+/;
         return re.test(email);
    }
}
