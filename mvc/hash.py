import random
import string


class Encryption:
    """
      This is a keyed Caesar cipher encryption and decryption class
    """
    # A list of all ascii letters and digits - A-Z and a-z and 0-9
    __letter_digit_list = [i for i in string.ascii_letters + string.digits]

    # Constructor method
    def __init__(self, data):
        # The data that has to be encrypted or decrypted
        self.data = data

    @staticmethod
    def search_and_replace(search_text, search_from_arrayay, replace_with_arrayay, recursion=0):
        # A nested function, that will find the element in the search arrayay
        def search_replace_element(search_elem, search_arrayay, replace_arrayay):
            # Linear search
            if search_elem in search_arrayay:
                # Getting the index of that search_elem situated in the search_arrayay list
                index = search_arrayay.index(search_elem)
                # Finding the respective element from the replace_arrayay list using the index
                return replace_arrayay[index]
            else:
                return search_elem

        # Recursion
        if recursion == len(search_text):
            return ""
        else:
            # Recursive method to get the encrypted data
            return search_replace_element(search_text[recursion], search_from_arrayay, replace_with_arrayay) \
                   + Encryption.search_and_replace(search_text,
                                                   search_from_arrayay,
                                                   replace_with_arrayay,
                                                   recursion + 1)

    def encrypt(self):
        """
        Keyed Caesar Cipher Encryption

        First we create a random key from ascii letters (Lowercase and Uppercase respectively) and digits(0-9)
        The key will be 6 digits
        Then we converted our secret key into a list -> key_char_list
        Then we remove key_char_list elements from our letter_digit_list and make a new list
            -> encrypted_letter_digit_list
        Then we put our key_char_list elements in the beginning
        E.G:
            letter_digit_list           = [a,b,c,d,e,1,2,3,4,5,...]
            key                         = be23
            key_char_list               = [b,e,2]
            encrypted_letter_digit_list = [b,e,2,3,a,c,d,1,4,5,...]

        here, letter_digit_list length === encrypted_letter_digit_list length

        letter_digit_list[0]            -> a
        encrypted_letter_digit_list[0]  -> b

        letter_digit_list[1]            -> b
        encrypted_letter_digit_list[1]  -> e

        letter_digit_list[n]            -> letter_digit_list elem
        encrypted_letter_digit_list[n]  -> encrypted_letter_digit_list elem

        This follows

        Then we loop through our given data, which we will encrypt We will change the data's character order using
        the encrypted_letter_digit_list
        E.G:
          data = bad23
          we will loop through our data
          In the first loop,
          we will get 'b' as instance Then we search 'b' in letter_digit_list and get the index of 'b' in the list Then
          [linear search]
          we will find the changed character/encryption character in the encrypted_letter_digit_list using that index
          [linear search]
          So index of 'b' in letter_digit_list is 1
          and encrypted_letter_digit_list[1] is e
          so we will replace b with e
          Then we will save that replaced character in a variable
          Then the loop will continue till string end
          Then we will an encrypted data with the changed letter digit order
          bad23 = eb3d1
          For later decryption we will add _$&k={key} at the end of the encrypted data
          So our final encrypted data will be eb3d1_$&k=be23
        """

        # Creating a random 6 digit Encryption Key

        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

        # Converting the string into an arrayay of the string's characters

        key_char_list = [i for i in key]
        letter_digit_list = self.__letter_digit_list

        # Making a new list that will remove the key_char_list element from the letters and digit list and bring that
        # key_char_list element in the front

        encrypted_letter_digit_list = key_char_list + [i for i in letter_digit_list if i not in key_char_list]

        # Encrypting the data
        updated_data = self.search_and_replace(self.data, letter_digit_list, encrypted_letter_digit_list)
        # Final encrypted data
        encrypted_data = f"{updated_data}_$&k={key}"
        return encrypted_data

    def decrypt(self):
        """
        Decryption is the reverse method of the encryption method
        First we will get the secret key from our data
        E.G:
            data = eb3d1_$&k=be23
        Now we will get our secret key from the data, _$&k={key}
        In the example, key is be23
        Now we will make a list from it
        Then we will make a list of encrypted_letter_digit_list and it will be similar to the encrypt method
        We will follow the same method as in encrypt
        But we will toggle encrypted_letter_digit_list with letter_digit_list to get our decrypted data
        """
        # Getting the key from the given data
        key = self.data.split("_$&k=")[-1]
        # Making a list of character from the key
        key_char_list = [i for i in key]
        # Copying the list of letters and digits
        letter_digit_list = self.__letter_digit_list
        # Making a new list that will remove the key_char_list element from the letters and digit list and bring that
        # key_char_list element in the front
        encrypted_letter_digit_list = key_char_list + [i for i in letter_digit_list if i not in key_char_list]
        # Removing the key from our data
        data = self.data.replace("_$&k=" + key, '')
        decrypted_data = self.search_and_replace(data, encrypted_letter_digit_list, letter_digit_list)
        return decrypted_data
