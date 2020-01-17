from django_otp.oath import TOTP
from django_otp.util import random_hex
from unittest import mock
import time
from mail import mailer
from django.http import JsonResponse

class TOTPVerification:

    def __init__(self):
        # secret key that will be used to generate a token,
        # User can provide a custom value to the key.
        self.key = random_hex(20)
        print(self.key)
        # counter with which last token was verified.
        # Next token must be generated at a higher counter value.
        self.last_verified_counter = -1
        # this value will return True, if a token has been successfully
        # verified.
        self.verified = False
        # number of digits in a token. Default is 6
        self.number_of_digits = 6
        # validity period of a token. Default is 30 second.
        self.token_validity_period = 120        #change to 15 mins..currently 60 secs

    def totp_obj(self):
        # create a TOTP object
        totp = TOTP(key=self.key,
                    step=self.token_validity_period,
                    digits=self.number_of_digits)
        # the current time will be used to generate a counter
        totp.time = time.time()
        print('inside definition of totp',totp.time)
        return totp

    def generate_token(self):
        # get the TOTP object and use that to create token
        totp = self.totp_obj()
        # token can be obtained with `totp.token()`
        token = str(totp.token()).zfill(6)
        print('token : ')
        print(token)
        return token

    def verify_token(self, token, tolerance,valid_time):
        if tolerance:
            tolerance=20000
        else:
            tolerance=0
       # tolerance = tolerance or 0
        print('inside verify_token:')

        try:
            # convert the input token to integer
            #token = int(token)
            print('inside try',token)

            token=token
        except ValueError:
            # return False, if token could not be converted to an integer
            print('return False, if token could not be converted to an integer')
            self.verified = False
        else:
            print('I am here inside else')
            print(valid_time)
            print(time.time())
            #totp = self.totp_obj()
            if valid_time<=time.time():
                totp=self.totp_obj()
            else:
                return JsonResponse('Time Out!!!!!')# check if the current counter value is higher than the value of
            # last verified counter and check if entered token is correct by
            # calling totp.verify_token()
            print('ibnside else',token)
            print(totp.t())
            print(tolerance)
            print((totp.verify(token, tolerance=tolerance)))
            print(self.last_verified_counter)
            if ((totp.t() > self.last_verified_counter) and
                    (totp.verify(token, tolerance=tolerance))):
                print('if the condition is true, set the last verified counter value to current counter value, and return True if the condition is true, set the last verified counter value to current counter value, and return True')
                self.last_verified_counter = totp.t()
                self.verified = True
            else:
                # if the token entered was invalid or if the counter value
                # was less than last verified counter, then return False
                print('# if the token entered was invalid or if the counter value was less than last verified counter, then return False')
                self.verified = False
        print(token,tolerance,self.verified)
        return self.verified


def forgotDef(email,otp,gen_time):
    # verify token the normal way
    print('###########  inside forgotDef of forgot_pwd')
    phone1 = TOTPVerification()
    print(phone1)



    #emails=['anjirwt8755@gmail.com']
    #username='TESTFORGOT'
    #body_temp="<b>Hello "+username+" ,</b> <br><p> <span style = 'color :blue ;' >Welcome to DAVID</span> your otp is </p><br><p>Have a great day ahead !</p><br><p>Thanks and Regards</p><br><p>DAVID</p>"
    #sub_temp="Successfully sent FORGOT REQUEST"
    #print("Generated token is: ", generated_token)
    #token = int(input("Enter token: "))

    #    print(phone1.verify_token(otp))
    #    return phone1.verify_token(otp)
    # verify token by passing along the token validity period.
    if email and otp==False and gen_time==False:
        print('inisde email')
        with mock.patch('time.time', return_value=1497657600):
            print("Current Time is: ", time.time())
            generated_token = phone1.generate_token()
            print(generated_token)
        return generated_token,time.time()
    if email==False and otp and gen_time:
        print('inside otp',otp)
        print(gen_time)
        with mock.patch('time.time',return_value=gen_time + phone1.token_validity_period):
            print('return_value of time',gen_time + phone1.token_validity_period)
            return_value=gen_time + phone1.token_validity_period
            print("Checking time after the token validity period has passed."
                  " Current Time is: ", time.time())
            #token = int(input("Enter token: "))
            token=otp
            print(phone1.verify_token(token,return_value, 1))


if __name__ == '__main__':
    forgotDef()