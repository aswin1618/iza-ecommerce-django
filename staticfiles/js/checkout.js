$(document).ready(function () {
    //razorpay
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();

		var amount_paid=$('.total_amount').attr('total');
        var name =$('.name').attr('name');
        var email =$('.email').attr('email');
        var phone =$('.phone').attr('phone');
        var order_number =$('.order_number').attr('order_number');
        var token = $("[name='csrfmiddlewaretoken']").val();
        console.log(order_number);
       
        
        var options = {
            "key": "rzp_test_nCGq2eKcFYga3A",
            "amount": "100", 
            "currency": "INR",
            "name": "IZA",
            "description": "Thank you for shopping wit us",
            "image": "https://example.com/your_logo",
            "handler": function (response){
                // alert(response.razorpay_payment_id);
                data = {
                    "payment_mode":"Paid by Razorpay",
                    "payment_id": response.razorpay_payment_id, 
                    "order_number":order_number,
                    "amount_paid":amount_paid, 
                    "csrfmiddlewaretoken":token,
                }
                console.log(data)
                $.ajax({
                    type: "POST",
                    url: "/orders/payments/",
                    data: data,
                    success: function (responsec) {
                        Swal.fire(
                                'Congratulations!',
                                responsec.status,
                                'success'
                            ).then((value) => {
                            window.location.href = '/orders/order_complete'+'?order_number='+order_number
                            console.log(order_number)

                          });

                    }
                });
                
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

        console.log('this is something', amount_paid);
        //ajax start
        data = {
            "payment_mode":"Cash on delivery", 
            "order_number":order_number,
            "amount_paid":amount_paid,
            // "payment_id": 'None', 
            "csrfmiddlewaretoken":token

        }
        console.log(data)
        $.ajax({
            type: "POST",
            url: "/orders/payments/",
            data: data,
            success: function (responsec) {
                Swal.fire(
                    'Congratulations!',
                    responsec.status,
                    'success'
                ).then((value) => {
                    window.location.href = '/orders/order_complete'+'?order_number='+order_number
                    console.log(order_number)

                  });

            }
        });



        
    });
});