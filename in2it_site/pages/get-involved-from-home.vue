<template>
    <div class="container">
        <h1 class="get-involved-title">Get involved, even from home!</h1>
        <h2 class="get-involved-subtitle">Some awesome projects that you can contribute to from home.</h2>

        <v-card v-for="project in projects" :key="project.id" class="d-flex mt-4">
            <v-row>
                <v-col cols="12" lg="6" sm="12">
                    <v-card-title class="project-title">
                        {{ project.title }}
                    </v-card-title>
                    <v-card-subtitle class="project-subtitle">
                        {{ project.subtitle }}
                    </v-card-subtitle>
                    <v-card-subtitle class="project-location">
                        Impact Region: {{ project.location }}
                    </v-card-subtitle>
                    <v-card-text class="project-description">
                        {{ project.description }}
                    </v-card-text>
                    <v-card-text class="project-url">
                        <a :href="project.projectUrl" _target="blank" class="learn-more-link">
                            Learn More
                            <img class='outgoing-link-icon' src='https://img.icons8.com/metro/26/000000/external-link.png'>
                        </a>
                    </v-card-text>
                </v-col>
                <v-col cols="12" lg="6" sm="12" align-self="center">
                    <a :href="project.projectUrl">
                        <v-img class="project-image" :src="project.imageUrl"></v-img>
                    </a>
                </v-col>
            </v-row>
        </v-card>
    </div>
</template>

<script>
export default {
    data () {
        return {
            projects: [
                {
                    title: 'My Block My Hood My City',
                    subtitle: 'Wellness calls for seniors',
                    location: 'Chicago',
                    description: 'My Block My Hood My City will be ensuring seniors have access to hand sanitizer, health supplements, toiletries, and food. Seniors and those living with disability are most at risk in the event of the continued spread of the virus. Volunteers can sign up to do wellness check-in calls for seniors.',
                    projectUrl: 'https://www.formyblock.org/viralresponse',
                    imageUrl: 'img/for-my-block.png'
                },
                {
                    title: 'The Newberry',
                    subtitle: 'Transcribing',
                    location: 'Chicago',
                    description: "Newberry Transcribe lets you contribute to historical scholarship, while learning about the everyday lives of individuals from a wide variety of backgrounds in the 19th and early 20th centuries. By transcribing handwritten letters, diaries, and other materials from the Newberry's Modern Manuscript Collections, you're helping to preserve these voices from the past - making their stories easier to find, search, and read.",
                    projectUrl: 'https://publications.newberry.org/digital/mms-transcribe/index',
                    imageUrl: 'img/newberry-transcribe.png'
                },
                {
                    id: 0,
                    title: 'Zooniverse',
                    subtitle: 'People-Powered Research',
                    location: 'Worldwide',
                    description: "The Zooniverse is the world's largest and most popular platform for people-powered research. This research is made possible by volunteers - hundreds of thousands of people around the world who come together to assist professional researchers. Their goal is to enable research that wouldn't be possible, or practical, otherwise. Zooniverse research results in new discoveries, datasets useful to the wider research community and many publications.",
                    projectUrl: 'https://www.zooniverse.org/projects',
                    imageUrl: 'img/zooniverse.png'
                },
                {
                    title: 'Foldit',
                    subtitle: 'Crowdsourced Research Games',
                    location: 'National',
                    description: "Foldit is a revolutionary crowdsourcing computer game enabling you to contribute to important scientific research. We're collecting data to find out if humans' pattern-recognition and puzzle-solving abilities make them more efficient than existing computer programs at pattern-folding tasks. If this turns out to be true, we can then teach human strategies to computers and fold proteins faster than ever!",
                    projectUrl: 'https://fold.it/portal/puzzles',
                    imageUrl: 'img/fold-it.jpg'
                },
                
                {
                    title: 'Crisis Text Line',
                    subtitle: 'Become a Crisis Counselor',
                    location: 'National',
                    description: "Crisis Text Line is the free, 24/7 text line for people in crisis in the United States. The service is powered by volunteer Crisis Counselors who work remotely—anywhere with a computer and secure internet connection works. Crisis Counselors answer texts from people in crisis, bringing them from a hot moment to a cool calm through active listening, collaborative problem solving, and safety planning.",
                    projectUrl: 'https://www.crisistextline.org/become-a-volunteer/',
                    imageUrl: 'img/crisis-text-line.png'
                }
            ]
        };
    }
}
</script>

<style scoped>
    .get-involved-title{
        font-size:48px;
        text-align: center;
    }
    .get-involved-subtitle{
        text-align: center;
    }
    .project-title{
        font-size:30px;
    }
    .project-subtitle{
        margin-top:4px;
        font-size:24px;
    }
    .project-location{
        font-size:20px;
        margin-top:0px;
        padding-top:0px;
    }
    .project-description{
        font-size:18px;
    }
    .project-image{
        margin:10px;
    }

    .project-url{
        padding:0px 15px 0px 15px;
        font-size:20px;
    }

    .learn-more-link{
        color:#173450;
    }

    .learn-more-link:hover{
        color:#4ec0c5;
    }

    .outgoing-link-icon{
        margin-top:-4px;
        margin-left:4px;
        height:15px;
        width:15px;
    }

    @media(max-width:767px){
        .project-image{
            max-width:500px;
        }
    }

    @media(max-width:691px){
        .project-image{
            min-width:400px;
            max-width:450px;
            margin-left:auto;
            margin-right:auto;
        }
    }

    @media(max-width:414px){
        .project-image{
            min-width:250px;
            max-width:340px;
            margin-left:auto;
            margin-right:auto;
        }
    }

    @media(max-width:320px){
        .project-image{
            min-width:180px;
            max-width:280px;
            margin-left:auto;
            margin-right:auto;
        }
    }
</style>