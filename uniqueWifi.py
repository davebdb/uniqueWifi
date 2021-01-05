#!/usr/bin/env python3

def main():
    import datetime
    import smtplib
    from subprocess import check_output
    from email.message import EmailMessage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Define the email addresses to be used
    fromEmailAddress = ''
    toEmailAddress = '' #multiple email addresses comma separated
    
    # find the year and month of last month and place it into formattedLastMonth variable
    today = datetime.date.today()
    firstDay = today.replace(day=1)
    lastMonth = firstDay - datetime.timedelta(days=1)
    formattedLastMonth = lastMonth.strftime("%Y%m")
    print(formattedLastMonth)

    # using the data from last month, find the number of wireless devices and set the value of output to that value and convert it to a string 
    output = check_output("/bin/grep \"IP: 10\.6\.\" /home/rsyslog/dhcp*-" + str(formattedLastMonth) + "*.log | /usr/bin/awk \'{print $10}\' | /usr/bin/sort -u | /usr/bin/wc -l", shell=True)
    output = str(output,'utf-8')
    print(output)

    # create the string to be sent in email
    uniqueWifiDevicesString = "The number of unique WIFI devices for " + str(formattedLastMonth) + " is: " + output

    # set up email MIME message and attach the text version of the string
    msg = MIMEMultipart()
    msg['From'] = fromEmailAddress
    msg['To'] = toEmailAddress
    msg['Subject'] = 'Unique WiFi Devices for ' + str(formattedLastMonth)
    part1 = MIMEText(uniqueWifiDevicesString,'plain')
    msg.attach(part1)

    # send the email out to recipients
    s=smtplib.SMTP('localhost')
    s.sendmail(msg["From"],msg["To"].split(","),msg.as_string())

if __name__ == "__main__":
    main()
