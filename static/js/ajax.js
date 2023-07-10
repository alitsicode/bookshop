

function increment(item) {
    // item is an argument that sent by plus/minus btn in template to choose product that we click
    document.getElementById(item).stepUp();
}
function decrement(item) {   
//  item is an argument that sent by plus/minus btn in template to choose product that we click
    document.getElementById(item).stepDown();
}