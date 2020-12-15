function recaptcha_resize(){
    // Need to upgrade...
    if (document.getElementsByClassName('g-recaptcha').length > 0)
    {
        pw = document.getElementsByClassName('g-recaptcha')[0].parentNode.clientWidth;
        cw = document.getElementsByClassName('g-recaptcha')[0].firstChild.clientWidth;
        scale = (pw) / (cw);
        document.getElementsByClassName('g-recaptcha')[0].style.transform = 'scale(' + scale + ')';
        document.getElementsByClassName('g-recaptcha')[0].style.transformOrigin = '0 0';
     }
};