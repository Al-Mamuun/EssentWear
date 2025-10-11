$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid"); // product id
    var quantitySpan = $(this).siblings('.quantity'); // quantity span

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            prod_id: id
        },
        success: function(data){
            if(data.status === 'success'){
                quantitySpan.text(data.quantity); // quantity update
                $('#amount').text(data.amount); // subtotal update
                $('#totalamount').text(data.totalamount); // total update
            } else {
                alert(data.message); // stock limit reached
            }
        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = $(this).siblings('.quantity'); // ✅ একইভাবে
    $.ajax({
       type: "GET",
       url: "/minuscart",
       data:{
           prod_id: id
       },
       success: function(data){
           eml.text(data.quantity)
           $('#amount').text(data.amount)
           $('#totalamount').text(data.totalamount)
       }
   })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = $(this)
    $.ajax({
       type: "GET",
       url: "/removecart",
       data:{
           prod_id: id
       },
       success: function(data){
           $('#amount').text(data.amount)
           $('#totalamount').text(data.totalamount)
           eml.closest('.cart-item').remove() // ✅ parent div remove
       }
   })
})

