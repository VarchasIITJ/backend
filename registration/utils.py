import random
import string


def random_string_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_referral_code():
    return "RG{rand_letters}{rand_digits}".format(rand_letters=random_string_generator(3, string.ascii_uppercase),
                                                  rand_digits=random.randint(10, 99))


def unique_ca_referral_code(instance, new_referral_code=None):
    if new_referral_code is not None:
        referral_code = new_referral_code
    else:
        referral_code = get_referral_code()

    klass = instance.__class__
    qs_exists = klass.objects.filter(referral_code=referral_code).exists()
    if qs_exists:
        new_referral_code = get_referral_code()
        return unique_ca_referral_code(instance, new_referral_code=new_referral_code)
    return referral_code
