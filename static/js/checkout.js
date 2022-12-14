$(document).ready(function () {
    // payment with razorpay
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();

		var amount_paid=$('.total_amount').attr('total');
        var name =$('.name').attr('name');
        var email =$('.email').attr('email');
        var phone =$('.phone').attr('phone');
        var order_number =$('.order_number').attr('order_number');
        var token = $("[name='csrfmiddlewaretoken']").val();
       
        
        var options = {
            "key": "rzp_test_nCGq2eKcFYga3A", // Enter the Key ID generated from the Dashboard
            "amount": "100", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "IZA",
            "description": "Thank you for shopping wit us",
            "image": "https://example.com/your_logo",
            // "order_id": order_number, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
            "handler": function (response){
                // alert(response.razorpay_payment_id);
                data = {
                    "payment_mode":"Paid by Razorpay",
                    "payment_id": response.razorpay_payment_id, 
                    "order_number":order_number,
                    "amount_paid":amount_paid, 
                    "csrfmiddlewaretoken":token
                }
               
                
            },
            "prefill": {
                "name": name,
                "email": email,
                "contact": phone
            },
            "notes": {
                "address": "Razorpay Corporate Office"
            },
            "theme": {
                "color": "#3399cc"
            }
        };
        var rzp1 = new Razorpay(options);
        rzp1.open();
    });// end of razorpay payment

    //cash on delivery
    $('.cod').click(function (e) { 
        e.preventDefault();
        var amount_paid=$('.total_amount').attr('total');
        var order_number =$('.order_number').attr('order_number');
        var token = $("[name='csrfmiddlewaretoken']").val();
        console.log(order_number)


        //ajax start
        data = {
            "payment_mode":"Cash on delivery", 
            "order_number":order_number,
            "amount_paid":amount_paid,
            // "payment_id": 'None', 
            "csrfmiddlewaretoken":token

        }
       



        
    });
});