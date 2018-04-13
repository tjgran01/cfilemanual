/* ADD THIS FILE TO YOUR QUALTRICS QUESTIONS TO SET MARKS UP. */
/* MARKS FOR fNIRS CAN BE [A-J]. */
/* THE FINAL MARK - SENT TO CLOSE THE CONNECTION SHOULD BE 'KILL' */

var mark = "A \n"

Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/

});

Qualtrics.SurveyEngine.addOnReady(function()
{
	/*Place your JavaScript here to run when the page is fully displayed*/

});

Qualtrics.SurveyEngine.addOnUnload(function()
{
		jQuery.ajax({
			type: "post",
   			url: "http://127.0.0.1:5000/mark",
			data: jQuery.param({mark: "A \n"}),
   			success: function(response) {
     			console.log("Red Wine! Success!")
   }

});
});
