<!-- PROJECT LOGO -->
<a href="https://www.linkedin.com/in/simon-mercier-372b6219b/">
  <img src="https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555">
  </a>
<p align="center">
  <h1 align="center">Reddit Post Video Maker</h1>

  <p align="center">
    Script that turns a Reddit post into a video
  <br/>
  <br/>
    <a href="https://www.youtube.com/watch?v=CihwNWMNfKQ&ab_channel=JustQuestions"><strong>Watch a demo (YouTube)</strong></a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [How it Works](#how-it-works) 
  * [Built With](#built-with)

<!-- ABOUT THE PROJECT -->
## About The Project

The YouTube algorithm often recommends me to watch videos that takes the most popular comments from a Reddit post and narrates them with text-to-speech. Seeing the millions of views these channels were gaining in a short period encouraged me to start a channel of my own.

I thought it would be a great idea to automate this laborious task of finding comments and editing every videos. 

This python script creates 5 to 10-minute-long videos in minutes with text-to-speech, transitions, animations, and background music ready to be uploaded to YouTube.

### How it Works

This is a quick explanation on how this tool works:
1. First, the script takes a screenshot and record a text-to-speech of the main post;
2. It will then sort the post's comments by "most upvotes" (most likes), to get the best comments;
3. Next, it takes a screenshot and record the autio of up to 30 comments that have more than 100 upvotes and less than 300 words;
4. It will also take a screenshot and record of up to 3 nested comments of main comment if they meet the same requirements as stated previously;
5. After that, it will combine every comments screenshoted with their audio and add transitions between the main comments;
6. Lastly, it adds video effects and background music and saves the video to a folder.

### Built With
I used Python 3 and these libraries:
* [Selenium WebDriver](https://www.selenium.dev/documentation/en/webdriver/)
* [FFmpeg](https://ffmpeg.org/)
* [moviepy](https://pypi.org/project/moviepy/)
