<template>
	<footer class="footer">
        <div class="container">
            <div class="container-fluid footer-container justify-content-end">
                <div>
                    <a href="https://chihacknight.org/" target="_blank">
                        <img src="/img/chihacknight-logo-light.png" class="chihacknight-logo" />
                    </a>
                    <p class="hacknight-project-label">A ChiHackNight project</p>
                </div>
            </div>
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
</style>