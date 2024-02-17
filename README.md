# Chotu Bot

Chotu is a Discord bot built with Nextcord and MongoDB. It has features like scheduling tasks, marking attendance, and handling messages in specific channels for Socrative Website.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of Python.
* You have a Windows/Linux/Mac machine.
* You have read the [Nextcord documentation](https://nextcord.readthedocs.io/en/latest/).
* You have a MongoDB Atlas account.

## Installing Chotu Bot

To install Chotu, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/udaysinh-git/Socrative-Attendance.git
```
2. Change into the directory:
```bash
cd Socrative-Attendance
```
3. Install the requirements:
```bash
pip install -r requirements.txt
```

## Using Chotu Bot

To use Chotu, you need to set up a few

 environment

 variables:

* `DISCORD_TOKEN`: Your Discord bot token.
* `MONGO_URI`: Your MongoDB connection string.
* `ATTENDANCE_CHANNEL`: The ID of the channel for marking attendance.
* `ATTENDANCE_REMOVAL_CHANNEL`: The ID of the channel for removing attendance.
* `ANNOUNCEMENT_CHANNEL`: The ID of the channel for announcements.

You can set these in a `.env` file in the root of your project:

```env
DISCORD_TOKEN=MTxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxx 
MONGO_URI=mongodb+srv://{username}:{Password}@xxxxx-xxxxxx.mongodb.net/admin
ATTENDANCE_CHANNEL=channel_id // where people will message for attendance
ATTENDANCE_REMOVAL_CHANNEL=channel_id // where people will message to revoke auto-attendance
ANNOUNCEMENT_CHANNEL=channel_id // Where bot will announce it has started marking attendance for room id
```

After setting up the environment variables, you can run the bot with:

```bash
python main.py
```

## Schedule Configuration
To configure the bot's schedule, you need to modify the schedule.csv file. The file should contain three columns: day, time, and room. The day should be the full name of the day (e.g., Monday), the time should be in 24-hour format (e.g., 16:13), and the room should be the room ID. It is recommended to set the time half an hour into the lecture to ensure the bot starts when there is a chance of having attendance.

Example:

```csv
day,time,room
Monday,16:13,TESTSOCRATIVE
```




## Contributing to Chotu Bot

To contribute to Chotu, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

## Contact

If you want to contact me you can reach me at `contact@udaysinh.me`.

## License

This project uses the following license: [Licenese](https://github.com/udaysinh-git/Socrative-Attendance/blob/main/LICENSE).
