��    g      T  �   �      �     �  �   �  �   �	     c
     y
  7   �
  U   �
  V     V   n  N   �  T     y   i  ^   �  y  B    �  �  �+     �?  <   �?     �?     @     @  0   "@     S@     c@     y@     @     �@  	   �@     �@  X   �@     A     +A     IA     ZA     _A     uA  %   �A     �A     �A  n   �A  Z   ;B     �B     �B  0   �B  	   �B  &   �B  &   C     CC     `C     pC     �C     �C     �C     �C     �C  ,   �C     D     D     D  .   ,D  +   [D  
   �D     �D     �D     �D      �D     �D  K   E  '   `E  -   �E     �E     �E  $   �E     F     F     +F     8F     JF  
   `F  )   kF  $   �F     �F     �F  #   �F  -   G     IG  2   PG  $   �G  U   �G  �   �G     �H  &   �H  (   �H  3   �H  
   )I  	   4I     >I  $   JI     oI     }I     �I  ]   �I  �  J     �K  [  �K    M     (N     >N  :   NN  U   �N  V   �N  V   6O  N   �O  T   �O  �   1P  b   �P  y  LQ  X  �Y  �  p  !   �  W   �  &   d�  #   ��     ��  \   ��     �     9�     X�     a�  (   ��     ��  
   ��  �   ǅ  ;   n�  ?   ��     �  
   ��  &   	�  $   0�  Q   U�     ��     ��  }   ԇ  �   R�     �  $   ��  k   �     ��  :   ��  .   Ӊ  $   �  !   '�  :   I�  :   ��  -   ��     �     ��     ��  u   �     }�     ��      ��  e   ɋ  H   /�  *   x�     ��  =   ��     ��  ?   �     Y�  �   x�  j   �  O   }�  %   ͎  ,   �  B    �     c�  %   q�     ��     ��  +   ��     �  J   �  8   O�  /   ��  1   ��  X   �  b   C�  
   ��  c   ��  ,   �  g   B�    ��  
   ȓ  b   ӓ  4   6�  s   k�     ߔ     �     ��  C   �  %   L�     r�     ��  ~   ��         V   "           +   X   5   [       =   7   ;         e              B       >          O   `       U   Q           C      b           I           4   -   E                            d   \   1           /       <   )       L   H   A   J   *   Y   S      ^      !   Z   T      ,   g   f   2      $      F   M   
          '                  %      (   :          K   .      N                        &   0   W   R   D           6   8             3   c          ]   _   G   P   9      #   a      	      ?      @    +1 650-123-4567 ,<br/><br/>
                                A password reset was requested for the Odoo account linked to this email.
                                You may change your password by following this link which will remain valid during 24 hours:<br/> ,<br/><br/>
                        A new device was used to sign in to your account. <br/><br/>
                        Here are some details about the connection:<br/> --<br/>Mitchell Admin 111.222.333.444 <span style="font-size: 10px;">Your Account</span><br/> <span style="font-weight: bold;">
                                    Browser:</span> <span style="font-weight: bold;">
                                    Location:</span> <span style="font-weight: bold;">
                                    Platform:</span> <span style="font-weight: bold;">
                                Date:</span> <span style="font-weight: bold;">
                                IP Address:</span> <strong>A password reset has been requested for this user. An email containing the following link has been sent:</strong> <strong>An invitation email containing the following subscription link has been sent:</strong> <table border="0" cellpadding="0" cellspacing="0" style="background-color: #FFFFFF; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;"><tr><td align="center">
<table border="0" cellpadding="0" cellspacing="0" width="590" style="padding: 16px; background-color: #FFFFFF; color: #454748; border-collapse:separate;">
<tbody>
    <!-- CONTENT -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <t t-set="invited_users" t-value="ctx.get('invited_users', [])"></t>
                <td style="text-align : left">
                    <span style="font-size: 20px; font-weight: bold;">
                        Pending Invitations
                    </span><br><br>
                </td>
                <tr><td valign="top" style="font-size: 13px;">
                    <div>
                        Dear <t t-out="object.name or ''">Mitchell Admin</t>,<br> <br>
                        You added the following user(s) to your database but they haven't registered yet:
                        <ul>
                            <t t-foreach="invited_users" t-as="invited_user">
                                <li t-out="invited_user or ''">demo@example.com</li>
                            </t>
                        </ul>
                        Follow up with them so they can access your database and start working with you.
                        <br><br>
                        Have a nice day!<br>
                        --<br>The <t t-out="object.company_id.name or ''">YourCompany</t> Team
                    </div>
                </td></tr>
                <tr><td style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
</tbody>
</table>
</td></tr>
</table>
             <table border="0" cellpadding="0" cellspacing="0" style="padding-top: 16px; background-color: #FFFFFF; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;"><tr><td align="center">
<table border="0" cellpadding="0" cellspacing="0" width="590" style="padding: 16px; background-color: #FFFFFF; color: #454748; border-collapse:separate;">
<tbody>
    <!-- HEADER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle">
                    <span style="font-size: 10px;">Welcome to Odoo</span><br>
                    <span style="font-size: 20px; font-weight: bold;">
                        <t t-out="object.name or ''">Marc Demo</t>
                    </span>
                </td><td valign="middle" align="right" t-if="not object.company_id.uses_default_logo">
                    <img t-attf-src="/logo.png?company={{ object.company_id.id }}" style="padding: 0px; margin: 0px; height: auto; width: 80px;" t-att-alt="object.company_id.name">
                </td></tr>
                <tr><td colspan="2" style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- CONTENT -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="top" style="font-size: 13px;">
                    <div>
                        Dear <t t-out="object.name or ''">Marc Demo</t>,<br><br>
                        You have been invited by <t t-out="object.create_uid.name or ''">OdooBot</t> of <t t-out="object.company_id.name or ''">YourCompany</t> to connect on Odoo.
                        <div style="margin: 16px 0px 16px 0px;">
                            <a t-att-href="object.signup_url" style="background-color: #875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;">
                                Accept invitation
                            </a>
                        </div>
                        <t t-set="website_url" t-value="object.get_base_url()"></t>
                        Your Odoo domain is: <b><a t-att-href="website_url" t-out="website_url or ''">http://yourcompany.odoo.com</a></b><br>
                        Your sign in email is: <b><a t-attf-href="/web/login?login={{ object.email }}" target="_blank" t-out="object.email or ''">mark.brown23@example.com</a></b><br><br>
                        Never heard of Odoo? It’s an all-in-one business software loved by 7+ million users. It will considerably improve your experience at work and increase your productivity.
                        <br><br>
                        Have a look at the <a href="https://www.odoo.com/page/tour?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;">Odoo Tour</a> to discover the tool.
                        <br><br>
                        Enjoy Odoo!<br>
                        --<br>The <t t-out="object.company_id.name or ''">YourCompany</t> Team
                    </div>
                </td></tr>
                <tr><td style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- FOOTER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; font-size: 11px; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle" align="left">
                    <t t-out="object.company_id.name or ''">YourCompany</t>
                </td></tr>
                <tr><td valign="middle" align="left" style="opacity: 0.7;">
                    <t t-out="object.company_id.phone or ''">+1 650-123-4567</t>
                    <t t-if="object.company_id.email">
                        | <a t-att-href="'mailto:%s' % object.company_id.email" style="text-decoration:none; color: #454748;" t-out="object.company_id.email or ''">info@yourcompany.com</a>
                    </t>
                    <t t-if="object.company_id.website">
                        | <a t-att-href="'%s' % object.company_id.website" style="text-decoration:none; color: #454748;" t-out="object.company_id.website or ''">http://www.example.com</a>
                    </t>
                </td></tr>
            </table>
        </td>
    </tr>
</tbody>
</table>
</td></tr>
<!-- POWERED BY -->
<tr><td align="center" style="min-width: 590px;">
    <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: #F1F1F1; color: #454748; padding: 8px; border-collapse:separate;">
      <tr><td style="text-align: center; font-size: 13px;">
        Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;">Odoo</a>
      </td></tr>
    </table>
</td></tr>
</table> <table border="0" cellpadding="0" cellspacing="0" style="padding-top: 16px; background-color: #FFFFFF; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;"><tr><td align="center">
<table border="0" cellpadding="0" cellspacing="0" width="590" style="padding: 16px; background-color: #FFFFFF; color: #454748; border-collapse:separate;">
<tbody>
    <!-- HEADER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle">
                    <span style="font-size: 10px;">Your Account</span><br>
                    <span style="font-size: 20px; font-weight: bold;">
                        <t t-out="object.name or ''">Marc Demo</t>
                    </span>
                </td><td valign="middle" align="right" t-if="not object.company_id.uses_default_logo">
                    <img t-attf-src="/logo.png?company={{ object.company_id.id }}" style="padding: 0px; margin: 0px; height: auto; width: 80px;" t-att-alt="object.company_id.name">
                </td></tr>
                <tr><td colspan="2" style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- CONTENT -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="top" style="font-size: 13px;">
                    <div>
                        Dear <t t-out="object.name or ''">Marc Demo</t>,<br><br>
                        Your account has been successfully created!<br>
                        Your login is <strong><t t-out="object.email or ''">mark.brown23@example.com</t></strong><br>
                        To gain access to your account, you can use the following link:
                        <div style="margin: 16px 0px 16px 0px;">
                            <a t-attf-href="/web/login?auth_login={{object.email}}" style="background-color: #875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;">
                                Go to My Account
                            </a>
                        </div>
                        Thanks,<br>
                        <t t-if="user.signature">
                            <br>
                            <t t-out="user.signature or ''">--<br>Mitchell Admin</t>
                        </t>
                    </div>
                </td></tr>
                <tr><td style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- FOOTER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; font-size: 11px; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle" align="left">
                    <t t-out="object.company_id.name or ''">YourCompany</t>
                </td></tr>
                <tr><td valign="middle" align="left" style="opacity: 0.7;">
                    <t t-out="object.company_id.phone or ''">+1 650-123-4567</t>
                    <t t-if="object.company_id.email">
                        | <a t-attf-href="'mailto:%s' % {{ object.company_id.email }}" style="text-decoration:none; color: #454748;"><t t-out="object.company_id.email or ''">info@yourcompany.com</t></a>
                    </t>
                    <t t-if="object.company_id.website">
                        | <a t-attf-href="'%s' % {{ object.company_id.website }}" style="text-decoration:none; color: #454748;">
                            <t t-out="object.company_id.website or ''">http://www.example.com</t>
                        </a>
                    </t>
                </td></tr>
            </table>
        </td>
    </tr>
</tbody>
</table>
</td></tr>
<!-- POWERED BY -->
<tr><td align="center" style="min-width: 590px;">
    <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: #F1F1F1; color: #454748; padding: 8px; border-collapse:separate;">
      <tr><td style="text-align: center; font-size: 13px;">
        Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;">Odoo</a>
      </td></tr>
    </table>
</td></tr>
</table> Already have an account? Another user is already registered using this email address. Authentication Failed. Back to Login Browser Cannot send email: user %s has no email address. Change password City, Region, Country Close Config Settings Confirm Password Confirmed Contact Could not contact the mail server, please check your outgoing email server configuration Could not create a new account. Could not reset your password Customer Account Dear Default Access Rights Don't have an account? Enable password reset from Login page Free sign up HTTP Routing If you do not expect this, you can safely ignore this email.<br/><br/>
                                Thanks, If you don't recognize it, you should change your password immediately via this link:<br/> In %(country)s Invalid signup token Let your customers log in to see their documents Marc Demo Multiple accounts found for this login Near %(city)s, %(region)s, %(country)s Near %(region)s, %(country)s Never Connected New Connection to your Account No account found for this login No login provided. OS Odoo On invitation Otherwise, you can safely ignore this email. Password Password Reset Password reset Password reset instructions sent to your email Passwords do not match; please retype them. Powered by Registration successful. Reminder for unregistered users Reset Password Send Password Reset Instructions Send an Invitation Email Sent automatically to admin if new user haven't responded to the invitation Sent to new user after you invited them Sent to portal user who registered themselves Settings: New Portal Signup Settings: New User Invite Settings: Unregistered User Reminder Sign up Signup Expiration Signup Token Signup Token Type Signup Token is Valid Signup URL Signup is not allowed for uninvited users Signup token '%s' is no longer valid Signup token '%s' is not valid Signup: invalid template user Signup: no login given for new user Signup: no name or partner given for new user Status Template user for new users created through signup The form was not properly filled in. There was an error when trying to deliver your Email, please check your configuration To send invitations in B2B mode, open a contact or select several ones in list view and click on 'Portal Access Management' option in the dropdown menu *Action*. User Users: Notify About Unregistered Users Welcome to {{ object.company_id.name }}! You cannot perform this action on an archived user. Your Email Your Name YourCompany day, month dd, yyyy - hh:mm:ss (GMT) e.g. John Doe http://www.example.com info@yourcompany.com {{ object.create_uid.name }} from {{ object.company_id.name }} invites you to connect to Odoo Project-Id-Version: Odoo Server 17.0
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2024-10-18 12:44+0330
Last-Translator: Mostafa Barmshory <mostafa.barmshory@gmail.com>, 2024
Language-Team: Persian (https://app.transifex.com/odoo/teams/41243/fa/)
Language: fa
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n > 1);
X-Generator: Poedit 3.2.2
 +1 650-123-4567 ,<br/><br/>
                                درخواستی برای بازنشانی رمز عبور حساب مرتبط با این ایمیل ارائه شد.
                                می‌توانید رمز عبورتان را با دنبال کردن این لینک که تا 24 ساعت معتبر است تغییر دهید<br/> ,<br/><br/>
                        یک دستگاه جدید برای ورود به حساب شما مورد استفاده قرار گرفته است. <br/><br/>
                        در اینجا جزئیاتی در مورد این ارتباط وجود دارد:<br/> --<br/>Mitchell Admin 111.222.333.444 <span style="font-size: 10px;">حساب شما</span><br/> <span style="font-weight: bold;">
                                    Browser:</span> <span style="font-weight: bold;">
                                    Location:</span> <span style="font-weight: bold;">
                                    Platform:</span> <span style="font-weight: bold;">
                                Date:</span> <span style="font-weight: bold;">
                                IP Address:</span> <strong>درخواست بازنشانی گذرواژه برای این کاربر انجام شده است. یک ایمیل شامل لینک زیر ارسال شده است:</strong> <strong>ایمیل دعوت شامل لینک عضویت زیر ارسال شده است:</strong> <table border="0" cellpadding="0" cellspacing="0" style="background-color: #FFFFFF; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;"><tr><td align="center">
<table border="0" cellpadding="0" cellspacing="0" width="590" style="padding: 16px; background-color: #FFFFFF; color: #454748; border-collapse:separate;">
<tbody>
    <!-- CONTENT -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <t t-set="invited_users" t-value="ctx.get('invited_users', [])"></t>
                <td style="text-align : left">
                    <span style="font-size: 20px; font-weight: bold;">
                        Pending Invitations
                    </span><br><br>
                </td>
                <tr><td valign="top" style="font-size: 13px;">
                    <div>
                        Dear <t t-out="object.name or ''">Mitchell Admin</t>,<br> <br>
                        You added the following user(s) to your database but they haven't registered yet:
                        <ul>
                            <t t-foreach="invited_users" t-as="invited_user">
                                <li t-out="invited_user or ''">demo@example.com</li>
                            </t>
                        </ul>
                        Follow up with them so they can access your database and start working with you.
                        <br><br>
                        Have a nice day!<br>
                        --<br>The <t t-out="object.company_id.name or ''">YourCompany</t> Team
                    </div>
                </td></tr>
                <tr><td style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
</tbody>
</table>
</td></tr>
</table>
             <table border="0" cellpadding="0" cellspacing="0" style="padding-top: 16px; background-color: #FFFFFF; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;"><tr><td align="center">
<table border="0" cellpadding="0" cellspacing="0" width="590" style="padding: 16px; background-color: #FFFFFF; color: #454748; border-collapse:separate;">
<tbody>
    <!-- HEADER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle">
                    <span style="font-size: 10px;">به پورتال RGERP خوش آمدید</span><br>
                    <span style="font-size: 20px; font-weight: bold;">
                        <t t-out="object.name or ''">Marc Demo</t>
                    </span>
                </td><td valign="middle" align="right" t-if="not object.company_id.uses_default_logo">
                    <img t-attf-src="/logo.png?company={{ object.company_id.id }}" style="padding: 0px; margin: 0px; height: auto; width: 80px;" t-att-alt="object.company_id.name">
                </td></tr>
                <tr><td colspan="2" style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- CONTENT -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="top" style="font-size: 13px;">
                    <div>
                         <t t-out="object.name or ''">Marc Demo</t>عزیز,<br><br>
                        شما توسط  <t t-out="object.create_uid.name or ''">ًربات</t>  <t t-out="object.company_id.name or ''">YourCompany شرکت </t>  جهت اتصال به پورتال RGERP دعوت‌شده‌اید .
                        <div style="margin: 16px 0px 16px 0px;">
                            <a t-att-href="object.signup_url" style="background-color: #875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;">
                                Accept invitation
                            </a>
                        </div>
                        <t t-set="website_url" t-value="object.get_base_url()"></t>
                        Your Odoo domain is: <b><a t-att-href="website_url" t-out="website_url or ''">http://yourcompany.odoo.com</a></b><br>
                        Your sign in email is: <b><a t-attf-href="/web/login?login={{ object.email }}" target="_blank" t-out="object.email or ''">mark.brown23@example.com</a></b><br><br>
                        Never heard of Odoo? It’s an all-in-one business software loved by 7+ million users. It will considerably improve your experience at work and increase your productivity.
                        <br><br>
                        Have a look at the <a href="https://www.odoo.com/page/tour?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;"> Tour</a> to discover the tool.
                        <br><br>
                        Enjoy Odoo!<br>
                        --<br>The <t t-out="object.company_id.name or ''">YourCompany</t> Team
                    </div>
                </td></tr>
                <tr><td style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- FOOTER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; font-size: 11px; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle" align="left">
                    <t t-out="object.company_id.name or ''">YourCompany</t>
                </td></tr>
                <tr><td valign="middle" align="left" style="opacity: 0.7;">
                    <t t-out="object.company_id.phone or ''">+1 650-123-4567</t>
                    <t t-if="object.company_id.email">
                        | <a t-att-href="'mailto:%s' % object.company_id.email" style="text-decoration:none; color: #454748;" t-out="object.company_id.email or ''">info@yourcompany.com</a>
                    </t>
                    <t t-if="object.company_id.website">
                        | <a t-att-href="'%s' % object.company_id.website" style="text-decoration:none; color: #454748;" t-out="object.company_id.website or ''">http://www.example.com</a>
                    </t>
                </td></tr>
            </table>
        </td>
    </tr>
</tbody>
</table>
</td></tr>
<!-- POWERED BY -->
<tr><td align="center" style="min-width: 590px;">
    <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: #F1F1F1; color: #454748; padding: 8px; border-collapse:separate;">
      <tr><td style="text-align: center; font-size: 13px;">
        Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;">Odoo</a>
      </td></tr>
    </table>
</td></tr>
</table> <table border="0" cellpadding="0" cellspacing="0" style="padding-top: 16px; background-color: #FFFFFF; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;"><tr><td align="center">
<table border="0" cellpadding="0" cellspacing="0" width="590" style="padding: 16px; background-color: #FFFFFF; color: #454748; border-collapse:separate;">
<tbody>
    <!-- HEADER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle">
                    <span style="font-size: 10px;">حساب شما</span><br>
                    <span style="font-size: 20px; font-weight: bold;">
                        <t t-out="object.name or ''">Marc Demo</t>
                    </span>
                </td><td valign="middle" align="right" t-if="not object.company_id.uses_default_logo">
                    <img t-attf-src="/logo.png?company={{ object.company_id.id }}" style="padding: 0px; margin: 0px; height: auto; width: 80px;" t-att-alt="object.company_id.name">
                </td></tr>
                <tr><td colspan="2" style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- CONTENT -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="top" style="font-size: 13px;">
                    <div>
                        Dear <t t-out="object.name or ''">Marc Demo</t>,<br><br>
                        حساب شما با موفقیت ایجاد شد!<br>
                        Your login is <strong><t t-out="object.email or ''">mark.brown23@example.com</t></strong><br>
                        برای دسترسی :
                        <div style="margin: 16px 0px 16px 0px;">
                            <a t-attf-href="/web/login?auth_login={{object.email}}" style="background-color: #875A7B; padding: 8px 16px 8px 16px; text-decoration: none; color: #fff; border-radius: 5px; font-size:13px;">
                                برو به حساب من 
                            </a>
                        </div>
                        Thanks,<br>
                        <t t-if="user.signature">
                            <br>
                            <t t-out="user.signature or ''">--<br>Mitchell Admin</t>
                        </t>
                    </div>
                </td></tr>
                <tr><td style="text-align:center;">
                  <hr width="100%" style="background-color:rgb(204,204,204);border:medium none;clear:both;display:block;font-size:0px;min-height:1px;line-height:0; margin: 16px 0px 16px 0px;">
                </td></tr>
            </table>
        </td>
    </tr>
    <!-- FOOTER -->
    <tr>
        <td align="center" style="min-width: 590px;">
            <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: white; font-size: 11px; padding: 0px 8px 0px 8px; border-collapse:separate;">
                <tr><td valign="middle" align="left">
                    <t t-out="object.company_id.name or ''">شرکت شما</t>
                </td></tr>
                <tr><td valign="middle" align="left" style="opacity: 0.7;">
                    <t t-out="object.company_id.phone or ''">+1 650-123-4567</t>
                    <t t-if="object.company_id.email">
                        | <a t-attf-href="'mailto:%s' % {{ object.company_id.email }}" style="text-decoration:none; color: #454748;"><t t-out="object.company_id.email or ''">info@yourcompany.com</t></a>
                    </t>
                    <t t-if="object.company_id.website">
                        | <a t-attf-href="'%s' % {{ object.company_id.website }}" style="text-decoration:none; color: #454748;">
                            <t t-out="object.company_id.website or ''">http://www.example.com</t>
                        </a>
                    </t>
                </td></tr>
            </table>
        </td>
    </tr>
</tbody>
</table>
</td></tr>
<!-- POWERED BY -->
<tr><td align="center" style="min-width: 590px;">
    <table border="0" cellpadding="0" cellspacing="0" width="590" style="min-width: 590px; background-color: #F1F1F1; color: #454748; padding: 8px; border-collapse:separate;">
      <tr><td style="text-align: center; font-size: 13px;">
        Powered by <a target="_blank" href="https://www.odoo.com?utm_source=db&amp;utm_medium=auth" style="color: #875A7B;">Odoo</a>
      </td></tr>
    </table>
</td></tr>
</table> از قبل حساب دارید؟ یک کاربر دیگر قبلا با این ایمیل ثبت نام کرده است. تایید هویت شکست خورد. بازگشت به صفحه ورود مرورگر وب نمی‌توان ایمیل فرستاد: کاربر %s نشانی ایمیلی ندارد. تغییر رمز عبور شهر، منطقه، کشور بستن تنظیمات پیکربندی رمز عبور را تایید کنید تایید شده مخاطب قادر به برقراری تماس با سرور ایمیل نیست، لطفاً پیکربندی سرور ایمیل ارسالی خود را بررسی کنید نمی‌توان یک حساب جدید ایجاد کرد. نمی‌توان گذرواژه شما بازنشانی کرد حساب مشتری گرامی حق دسترسی های پیش فرض حساب کاربری ندارید؟ فعالسازی درخواست تجدید رمز عبور از صفحه ورود ثبت نام آزاد مسیریابی HTTP اگر منتظر این ایمیل نبودید به راحتی آن را نادیده بگیرید.<br/><br/> با تشکر اگر آن را نمی‌شناسید، باید فوراَ رمز عبور خود را از طریق این لینک تغییر دهید: <br/> در %(country)s رمز ثبت نام غیر مجاز اجازه بدهید مشتری‌های شما وارد شوند تا اسناد خود را ببینند دموی مارچ چندین حساب برای این ورود یافت شد %(city)s، %(region)s، %(country)s نزدیک %(region)s، %(country)s نزدیک  هیچ وقت متصل نبوده برقراری ارتباط جدید با حساب شما  هیچ حسابی برای این ورود یافت نشد امکان ورود مهیا نشده است. OS اودو با دعوت در غیر این صورت، می‌توانید بدون مشکل این ایمیل را نادیده بگیرید. گذرواژه بازنشانی ایمیل بازنشانی رمز عبور دستورالعمل‌های بازنشانی رمز عبور به ایمیل شما ارسال شد گذرواژه مطابقت ندارد؛ دوباره تلاش کنید. راه اندازی شده به وسیله ثبت نام موفق. یادآوری برای کاربران ثبت نام نشده بازنشانی گذرواژه ارسال دستورالعمل بازنشانی گذرواژه ارسال ایمیل دعوت در صورتی که کاربر جدید به دعوت‌نامه پاسخ ندهد، به صورت خودکار به ادمین ارسال می‌شود پس از اینکه آنها را دعوت کردید، به کاربر جدید ارسال می‌شود به کاربر پورتال که ثبت نام کرده است ارسال شد عضویت جدید در پورتال تنظیمات: دعوت کاربر جدید تنظیمات: پیام یادآوری کاربر ثبت نشده ثبت نام تاریخ انقضاء ثبت نام رمز ثبت نام نوع ثبت نام عملیات ثبت نام فعال است. لینک ثبت نام ثبت نام برای کاربران دعوت نشده مجاز نیست. توکن ثبت نام '%s' دیگر معتبر نیست توکن ثبت نام '%s' معتبر نیست ثبت نام: کاربر قالب نامعتبر ثبت نام: هیچ لاگینی برای کاربر جدید داده نشده است ثبت نام: هیچ نام یا شریکی برای کاربر جدید داده نشده است وضعیت کاربری موقت برای کاربران جدید از طریق ثبت نام انجام شد. فرم به درستی پر نشده است. هنگام ارسال ایمیل خود، لطفاً پیکربندی‌تان را بررسی کنید برای ارسال دعوت نامه‌ها در حالت B2B، یک مخاطب را باز کنید یا چند مورد را در لیست‌مشاهده انتخاب کنید و روی گزینه 'Portal Access Management' در منوی بازشدنی اقدام کلیک کنید. کاربر کاربران: در مورد کاربران ثبت نام نشده اطلاع رسانی کنید به {{ object.company_id.name }} خوش آمدید! شما نمی توانید این اقدام را روی یک کاربر بایگانی شده انجام دهید. ایمیل شما نام شرکت شما روز، ماه، سال، ساعت، دقیقه، ثانیه (GMT) برای مثال محمد احمدی http://www.example.com info@yourcompany.com ${object.create_uid.name} از ${object.company_id.name} شما را دعوت می کند تا به اودو متصل شوید 