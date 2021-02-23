<template>
	<nav class="navbar navbar-expand-lg navbar-light in2it-navbar">
        <div class="container">
            <div class="navbar-container">
                <a class="in2it-brand" href="/">
                    <img class="navbar-logo" src="/img/in2it-logo.png">
                </a>
                <div class="in2it-nav-link-group">
                    <a class="in2it-nav-link" href="/events">Map</a>
                    <a class="in2it-nav-link" href="/about-us">About Us</a>
                    <a class="in2it-nav-link" href="/join-us">Join Us</a>
                    <a class="in2it-nav-link" href="/login">Log In</a>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
	export default{};
</script>

<style scoped>
    .in2it-navbar{
        color:#173450;
        height:120px;
    }

    .navbar-container{
        width:100%;
        display: flex;
        flex-direction: row;
    }

    .in2it-nav-link{
        display:flex;
        align-self: flex-end;
        padding:10px 20px 0px 20px;
        color:#173450;
        font-size:24px;
        font-weight:bold;
        line-height: 75px;
        transition: 0.3s;
        white-space: nowrap;
    }

    .in2it-nav-link:hover{
        text-decoration: none;
        color:#4ec0c5;
    }

    .in2it-nav-link-group{
        display:flex;
        flex-direction: row;
        margin-left: auto;
    }

    .in2it-brand{
        line-height:91px;
    }

    .logo-container{
        padding:0px;
        height: 60px;
        margin-left:20px;
    }

    .navbar-logo{
        width:26vw;
        max-width: 200px;
        margin-right:20px;
    }

    @media (max-width: 768px) {
        .in2it-nav-link{
            font-size:18px;
            padding:5px 10px 0px 10px;
        }
    }

    @media (min-width: 769px) and (max-width: 991px) {
        .in2it-nav-link{
            font-size:20px;
            padding:7px 15px 0px 15px;
        }
    }
</style>