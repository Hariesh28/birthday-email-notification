
# Birthday Celebration Notification System

This project is designed to send birthday notifications via email based on the data provided in a CSV file. It also checks for new email requests and responds accordingly.

## Features

- Check for student birthdays and send email notifications.
- Respond to email requests for the birthday list.
- Scheduled tasks for sending daily notifications.
- Multi-threaded email checking.

## Requirements

- Python 3.x
- The following Python libraries:
  - datetime
  - json
  - smtplib
  - os
  - email
  - imaplib
  - threading
  - schedule
  - time
  - pandas

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Hariesh28/birthday-email-notification.git
   cd birthday-email-notification
   ```

2. **Install the required Python libraries:**

   ```bash
   pip install pandas schedule
   ```

3. **Set up the environment variables:**

   Set the `SPAM_G_ACC_APP_PASSWORD` environment variable with the password for your email account.

4. **Create a `constants.json` file with the following structure:**

   ```json
   {
     "sender_mail_id": "your_email@gmail.com",
     "receiver_mail_ids": ["receiver1@gmail.com", "receiver2@gmail.com"],
     "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
   }
   ```

5. **Prepare your `data.txt` file:**

   Ensure your `data.txt` file contains student data with the following columns: `dob`, `name`, `section`, `student_id`.

## Usage

1. **Run the script:**

   ```bash
   python main.py
   ```

2. The script will:
   - Check for student birthdays from the `data.txt` file and send email notifications.
   - Check for new email requests and respond with the birthday list if requested.
   - Send daily notifications at the scheduled time.

## Classes and Methods

### `BirthDay`

- `get_student_info(dataframe: pd.DataFrame) -> list[dict] | None`
  - Extracts student information and checks if today is their birthday.

### `mail`

- `load_constants() -> dict`
  - Loads constants from the `constants.json` file.
- `get_message(data: list[dict] | None) -> str`
  - Generates the email message content.
- `send_mail(data: list[dict] | None, receivers_address: list[str]) -> bool`
  - Sends the email notification.

### `readEmail`

- `get_constant_data() -> dict`
  - Loads constants from the `constants.json` file.
- `sign_in()`
  - Signs in to the email account.
- `sign_out()`
  - Signs out of the email account.
- `get_no_of_emails() -> int`
  - Returns the number of emails in the inbox.
- `check_for_new_email()`
  - Checks for new email requests.

### `master`

- `start_thread(func)`
  - Starts a new thread for the given function.
- `start_program()`
  - Starts the main program with scheduled tasks.

## Notes

- Ensure your email account has the necessary permissions and settings to allow sending emails via SMTP.
- Make sure the `data.txt` and `constants.json` files are correctly formatted and located in the same directory as the script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
