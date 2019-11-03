<template>
    <div>
        <div class="landing-page-title-container">
            <h1 class="landing-page-title">Make an impact in your</h1>
            <span class="slidingVertical landing-page-title">
                <span> Neighborhood</span>
                <span> Community</span>
                <span> City</span>
            </span>
        </div>
        <h2 class="landing-page-tagline">Find ways to get involved, contribute your skills, make a difference.</h2>
    </div>
</template>

<style scoped>
	/*Vertical Sliding*/
	.slidingVertical{
		display:flex;
		width:320px;
		margin-top:-60px;
	}
	.slidingVertical span{
		display:flex;
		animation: topToBottom 9s linear infinite 0s;
		-ms-animation: topToBottom 9s linear infinite 0s;
		-webkit-animation: topToBottom 9s linear infinite 0s;
		color: #4ec0c5;
		opacity: 0;
		overflow: hidden;
		position: absolute;
		margin-left:8px;
		padding:4px;
	}
	.slidingVertical span:nth-child(2){
		animation-delay: 3s;
		-ms-animation-delay: 3s;
		-webkit-animation-delay: 3s;
	}
	.slidingVertical span:nth-child(3){
		animation-delay: 6s;
		-ms-animation-delay: 6s;
		-webkit-animation-delay: 6s;
	}

	/*topToBottom Animation*/
    @-moz-keyframes topToBottom{
        0% { opacity: 0; }
        5% { opacity: 0; }
        15% { opacity: 1; }
        35% { opacity: 1; }
        45% { opacity: 0; }
        100% { opacity: 0; }
    }
    @-webkit-keyframes topToBottom{
        0% { opacity: 0; }
        5% { opacity: 0; }
        15% { opacity: 1; }
        35% { opacity: 1; }
        45% { opacity: 0; }
        100% { opacity: 0; }
    }
    @-ms-keyframes topToBottom{
        0% { opacity: 0; }
        5% { opacity: 0; }
        15% { opacity: 1; }
        35% { opacity: 1; }
        45% { opacity: 0; }
        100% { opacity: 0; }
    }

    @media (max-width: 768px) {
        .landing-page-title{
            font-size: 28px;
        }
        .landing-page-tagline{
            font-size: 20px;
        }
        .slidingVertical{
            margin-top:-25px;
        }
    }

    @media (min-width: 769px) and (max-width: 991px) {
        .landing-page-title{
            font-size: 38px;
        }
        .landing-page-tagline{
            font-size: 30px;
        }
        .slidingVertical{
            margin-top:-40px;
        }
    }
</style>