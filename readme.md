# Intervals ICU to github repo
### Download your intervals.icu fit files to a github repository. Or don't use the included github action, and just download it to your computer.

---

In order to protect the great resource that is Intervals ICU, we only downloading the last two days of files. The action should run nightly, so this should be plenty.

## Setup with Github actions

1. Create a github repository for your fit files. It is highly recormended that you use a private repo

2. In Intervals.icu settings, find your athleth ID and API key. If needed click on the pencil to create a key

![ alt text](/assets/intervals_settings.png)

3. Create an action secret for your repository called INTERVALS_ATHLETE_ID containing your Athlete ID

4. Create an action secret for your repository called INTERVALS_API_KEY containing your API key
