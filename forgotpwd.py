from django_otp.oath import TOTP
from django_otp.util import random_hex
from unittest import mock
import time


class TOTPVerification:

    def __init__(self):
        # secret key that will be used to generate a token,
        # User can provide a custom value to the key.
        self.key = random_hex(20)
        # counter with which last token was verified.
        # Next token must be generated at a higher counter value.
        self.last_verified_counter = -1
        # this value will return True, if a token has been successfully
        # verified.
        self.verified = False
        # number of digits in a token. Default is 6
        self.number_of_digits = 6
        # validity period of a token. Default is 30 second.
        self.token_validity_period = 35

    def totp_obj(self):
        # create a TOTP object
        totp = TOTP(key=self.key,
                    step=self.token_validity_period,
                    digits=self.number_of_digits)
        # the current time will be used to generate a counter
        totp.time = time.time()
        return totp

    def generate_token(self):
        # get the TOTP object and use that to create token
        totp = self.totp_obj()
        # token can be obtained with `totp.token()`
        token = str(totp.token()).zfill(6)
        return token

    def verify_token(self, token, tolerance=0):
        try:
            # convert the input token to integer
            print('convert the input token to integer')
            token = int(token)
        except ValueError:
            # return False, if token could not be converted to an integer
            print('return False, if token could not be converted to an integer')
            self.verified = False
        else:
            totp = self.totp_obj()
            print('inside else of verify_token and totp is:',totp)
            # check if the current counter value is higher than the value of
            # last verified counter and check if entered token is correct by
            # calling totp.verify_token()
            print('checking conditons in else')
            print(totp.t())
            print(self.last_verified_counter)
            print(totp.verify(token, tolerance=tolerance))
            if ((totp.t() > self.last_verified_counter)and
                    (totp.verify(token, tolerance=tolerance) )):
                print('if the condition is true, set the last verified counter value to current counter value, and return Tru')
                # if the condition is true, set the last verified counter value
                # to current counter value, and return True
                self.last_verified_counter = totp.t()
                self.verified = True
            else:
                print('if the token entered was invalid or if the counter value was less than last verified counter, then return False')
                # if the token entered was invalid or if the counter value
                # was less than last verified counter, then return False
                self.verified = False
        print(token,tolerance,self.verified)
        return self.verified


if __name__ == '__main__':
    # verify token by passing along the token validity period.
    phone1=TOTPVerification()
    print('now token will generate')
    with mock.patch('time.time', return_value=1497657600):
        print("Current Time is: ", time.time())
        generated_token = phone1.generate_token()
        print('print generated token is: ',generated_token)
    print('now token will get verified')
    with mock.patch(
        'time.time',
            return_value=1497657600 + phone1.token_validity_period):
        print("Checking time after the token validity period has passed."
              " Current Time is: ", time.time())
        token = int(input("Enter token: "))
        print(phone1.verify_token(token, tolerance=1))