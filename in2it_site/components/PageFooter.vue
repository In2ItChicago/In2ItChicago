<template>
    <footer class="footer">
        <div class="container-fluid footer-container justify-content-end">
            <div class="mt-2">
                <a href="https://chihacknight.org/" target="_blank">
                    <img src="/img/chihacknight-logo-light.png" class="chihacknight-logo" />
                </a>
                <p class="hacknight-project-label">A ChiHackNight project</p>
                <p class="privacy-terms-text">
                <a href="/terms-and-conditions">Terms & Conditions</a> | <a href="/privacy-policy">Privacy Policy</a>
            </p>
            </div>
        </div>
        <div class="container-fluid footer-container justify-content-start">
            
        </div>
    </footer>
</template>

<style scoped>
    .chihacknight-logo{
        height:65px;
        width:auto;
    }

    .footer{
        position: relative;
        bottom: 0;
        width: 100%;
        background-color:#173450;
    }

    .footer-container{
        display:flex;
    }

    .hacknight-project-label{
        color: #fff;
        font-size: 18px;
        font-family: 'Nunito', 'regular';
    }

    .privacy-terms-text, .privacy-terms-text a{
        color:#fff;
    }
</style>