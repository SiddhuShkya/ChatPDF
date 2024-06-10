# Define CSS styles
css = '''
<style>
.chat-message {
    padding: 1.5rem; 
    border-radius: 0.8rem; 
    margin-bottom: 1rem; 
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 15%;
}
.chat-message .avatar img {
    width: 78px;
    height: 78px;
    border-radius: 50%;
    object-fit: cover;
    object-position: center;
    overflow: hidden;
}
.chat-message .message {
    width: 85%;
    padding: 0 1.5rem;
    color: #fff;
    font-size: 18px;
}
</style>
'''
# Bot and user templates
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://t4.ftcdn.net/jpg/03/51/61/49/360_F_351614912_nhPej8tYdn8gytfBnBPag8HBUt2vaznE.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://www.shareicon.net/data/512x512/2016/09/15/829472_man_512x512.png" alt="User Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''