import feedparser
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse


def load_smtp_setings():
    smtp_server = os.getenv('smtp_server', 'load_from_file')
    smtp_port   = os.getenv('smtp_port')
    sender_mail = os.getenv('sender_mail')
    sender_pass = os.getenv('sender_pass')
    receiv_mail = os.getenv('receiv_mail')
    topic = os.getenv('topic')
    body  = os.getenv('body')
    if smtp_server == 'load_from_file':
        return load_smtp_setings_from_file()
    return smtp_server, smtp_port, sender_mail, sender_pass, receiv_mail, topic, body


def load_smtp_setings_from_file():
    cfgpath = "email_settings.txt"
    fconf = open(cfgpath, 'r')
    tconf = fconf.read()
    fconf.close()
    conf_list = tconf.split('\n')
    return conf_list[0], conf_list[1], conf_list[2], conf_list[3], conf_list[4], conf_list[5], conf_list[6]


def send_email(new_videos, sendmail_settings):
    # set up the SMTP server
    login = mail_settings[0]
    s = smtplib.SMTP_SSL(host=sendmail_settings[0], port=sendmail_settings[1])
    s.login(sendmail_settings[2], sendmail_settings[3])
    msg = MIMEMultipart()  # create a message
    message = sendmail_settings[6]+"\n"
    for every_video in new_videos:
        message = message+every_video[0]+" "+every_video[1]+"\n"
    # setup the parameters of the message
    msg['From'] = sendmail_settings[2]
    msg['To'] = sendmail_settings[4]
    msg['Subject'] = sendmail_settings[5]
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)
    print("email sent")
    del msg


def load_sent_items():
    p_items = "sent_items.txt"
    fitems = open(p_items, 'r')
    titems = fitems.read()
    fitems.close()
    sent_items = titems.split('\n')
    return sent_items


def write_items(items_to_write):
    items_path = "sent_items.txt"
    fitems = open(items_path, 'a')
    text_to_write = ""
    for every_item_name in items_to_write:
        text_to_write = text_to_write+every_item_name+"\n"
    fitems.write(text_to_write)
    fitems.close()


def get_rss(cold_start_opt, rss_mail_settings):
    rss_server = os.getenv('rss_server', 'load_from_file')
    if rss_server == 'load_from_file':
        cfgpath = "rss_source.txt"
        fconf = open(cfgpath, 'r')
        tconf = fconf.read()
        fconf.close()
        rss_server = tconf
    sent_items = load_sent_items()
    news_feed = feedparser.parse(rss_server)
    to_send = []
    to_write = []
    list_of_entries = news_feed.entries
    for entry in list_of_entries:
        if entry['title'] not in sent_items:
            to_send.append([entry['title'], entry['link']])
            to_write.append(entry['title'])
    if len(to_send) > 0 and not cold_start_opt:
        send_email(to_send, rss_mail_settings)
    if len(to_write) > 0:
        write_items(to_write)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--coldstart",
                        help="populate base before putting the script in cron",
                        action="store_true")
    args = parser.parse_args()
    print("starting RSS to email script")
    if args.coldstart:
        cold_start = True
    else:
        cold_start = False
    mail_settings = load_smtp_setings()
    get_rss(cold_start, mail_settings)
