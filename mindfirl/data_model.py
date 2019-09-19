import logging
import copy
import data_display as dd
from util import RET

NUM_ATTR = 11

class DataPair(object):
    """
    This class stores a pair of data, because in record linkage, many things is only meaningful for a pair of data
    The data in this object is data-dependent, not user-dependent, that means everything store in this object is common accross all users.
    """
    def __init__(self, data1_raw, data2_raw):
        """
        data_raw is the raw value of the data, for example:
            ['1','','206','NELSON','MITCHELL','1459','03/13/1975','M','B','','******','********___','03/13/1975','*','*','34','6','0'],
            ['1','1000142704, '174','NELSON','MITCHELL SR','1314','07/03/1949','M','B','1000142704','******','******** SR','07/03/1949','*','*','34','6','0']
        pair_num is the pair number of the data pair, it is the unique id for data pair
        data_attributes are the actual attributes, such as ID, Name, DoB, Gender, Race.
        data_helpers are the helpers that helps to calculate partial value of attributes, this is for internal use
        data_attributes_full: full disclosure
        data_attributes_partial: partial disclosure
        data_attributes_masked: masked disclosure
        icons: the supplemental markups
        ids: the id for each attribute, with the format - pair_num-row_num-attribute_num (1-1-0)
        data_attribute_types: data types, for now it is hard coded
        data_display: this is different from the data_attribute_display: this includes the name frequency, name swap and so on.
        """
        self.num_of_attr = 11

        self._data1_raw = data1_raw
        self._data2_raw = data2_raw
        self._pair_num = int(self._data1_raw[0])
        self._data1_attributes = list()
        self._data2_attributes = list()
        self._icons = list()
        self._data1_ids = list()
        self._data2_ids = list()
        self._data1_helpers = list()
        self._data2_helpers = list()
        self._data1_attributes_base = list()
        self._data1_attributes_full = list()
        self._data1_attributes_partial = list()
        self._data1_attributes_masked = list()
        self._data2_attributes_base = list()
        self._data2_attributes_full = list()
        self._data2_attributes_partial = list()
        self._data2_attributes_masked = list()
        self._data_attribute_types = ['string', 'string', 'string', 'date', 'character', 'character', 'character', 'character', 'character', 'character', 'character']
        self._data_display = dict()

        self._initialize_data()
        self._generate_icons()
        self._generate_ids()
        self._generate_data_attributes_display()
        self._generate_data_display()


    def _initialize_data(self):
        """
        put the data from raw data to formatted data structure
        """
        self._data1_attributes = []
        self._data2_attributes = []
        self._data1_helpers = []
        self._data2_helpers = []

        attribute_idx = [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]
        for i in attribute_idx:
            self._data1_attributes.append(self._data1_raw[i])
            self._data2_attributes.append(self._data2_raw[i])
        helper_idx = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        for i in helper_idx:
            self._data1_helpers.append(self._data1_raw[i])
            self._data2_helpers.append(self._data2_raw[i])


    def _generate_icons(self):
        self._icons = []
        self._icons = dd.generate_icon([self._data1_raw, self._data2_raw])[0]


    def _generate_ids(self):
        self._data1_ids = []
        self._data2_ids = []
        for i in range(self.num_of_attr):
            self._data1_ids.append(str(self._pair_num) + '-1-' + str(i))
            self._data2_ids.append(str(self._pair_num) + '-2-' + str(i))


    def _generate_data_attributes_display(self):
        self._data1_attributes_base = []
        self._data1_attributes_full = []
        self._data1_attributes_partial = []
        self._data1_attributes_masked = []
        self._data2_attributes_base = []
        self._data2_attributes_full = []
        self._data2_attributes_partial = []
        self._data2_attributes_masked = []

        for i in range(self.num_of_attr):
            if self._data_attribute_types[i] == 'string':
                get_display = dd.get_string_display
            elif self._data_attribute_types[i] == 'date':
                get_display = dd.get_date_display
            elif self._data_attribute_types[i] == 'character':
                get_display = dd.get_character_display
            else:
                # error: unsupported attribute type
                logging.error('unsupported attribute type.')

            display_base = get_display(
                attr1 = self._data1_attributes[i], 
                attr2 = self._data2_attributes[i], 
                helper1 = self._data1_helpers[i], 
                helper2 = self._data2_helpers[i], 
                attribute_mode='base'
            )
            self._data1_attributes_base.append(display_base[0])
            self._data2_attributes_base.append(display_base[1])

            display_full = get_display(
                attr1 = self._data1_attributes[i], 
                attr2 = self._data2_attributes[i], 
                helper1 = self._data1_helpers[i], 
                helper2 = self._data2_helpers[i], 
                attribute_mode='full'
            )
            self._data1_attributes_full.append(display_full[0])
            self._data2_attributes_full.append(display_full[1])

            display_partial = get_display(
                attr1 = self._data1_attributes[i], 
                attr2 = self._data2_attributes[i], 
                helper1 = self._data1_helpers[i], 
                helper2 = self._data2_helpers[i], 
                attribute_mode='partial'
            )
            self._data1_attributes_partial.append(display_partial[0])
            self._data2_attributes_partial.append(display_partial[1])

            display_masked = get_display(
                attr1 = self._data1_attributes[i], 
                attr2 = self._data2_attributes[i], 
                helper1 = self._data1_helpers[i], 
                helper2 = self._data2_helpers[i], 
                attribute_mode='masked'
            )
            self._data1_attributes_masked.append(display_masked[0])
            self._data2_attributes_masked.append(display_masked[1])

        # all the attributes has base, full, and masked mode, but not necessary partial mode
        for i in range(self.num_of_attr):
            if self._data1_attributes_partial[i] == self._data1_attributes_masked[i] and self._data2_attributes_partial[i] == self._data2_attributes_masked[i]:
                self._data1_attributes_partial[i] = None
                self._data2_attributes_partial[i] = None


    def _generate_data_display(self):
        data_mode = ['base', 'full', 'masked', 'minimum', 'moderate']
        for mode in data_mode:
            self._data_display[mode] = dd.format_data([self._data1_raw, self._data2_raw], mode)


    def attribute_match(self, i):
        return self._data1_attributes[i] == self._data2_attributes[i]

    def has_partial_mode(self, i):
        if i < 0 or i > self.num_of_attr:
            logging.error('Wrong attribute index: ' + str(i))
            return False
        return not (self._data1_attributes_partial[i] is None and self._data2_attributes_partial[i] is None)

    def get_attribute_display(self, i, attribute_mode):
        if i < 0 or i >= self.num_of_attr:
            logging.error('Error: attribute index not in range.')
            return RET(status=1, return_data='Error: attribute index not in range.')

        ret = list()
        if attribute_mode == 'base':
            ret = [self._data1_attributes_base[i], self._data2_attributes_base[i]]
        elif attribute_mode == 'full':
            ret = [self._data1_attributes_full[i], self._data2_attributes_full[i]]
        elif attribute_mode == 'partial':
            ret = [self._data1_attributes_partial[i], self._data2_attributes_partial[i]]
            if ret[0] is None:
                ret[0] = self._data1_attributes_masked[i]
            if ret[1] is None:
                ret[1] = self._data2_attributes_masked[i]
        elif attribute_mode == 'masked':
            ret = [self._data1_attributes_masked[i], self._data2_attributes_masked[i]]
        else:
            logging.error('Error: unsupported attribute mode.')
        return ret


    def get_data_display(self, data_mode):
        if data_mode not in ['base', 'full', 'masked', 'minimum', 'moderate']:
            logging.error('Error: unsupported data mode')
        return self._data_display[data_mode]


    def get_icons(self):
        return self._icons


    def get_attributes(self, i):
        if i not in range(self.num_of_attr):
            logging.error('Error: attribute index out of range.')
        return [self._data1_attributes[i], self._data2_attributes[i]]


    def get_helpers(self, i):
        if i not in range(self.num_of_attr):
            logging.error('Error: attribute index out of range.')
        return [self._data1_helpers[i], self._data2_helpers[i]]

    def get_next_display(self, attr_id, attr_mode):
        if attr_mode not in ['full', 'partial', 'masked', 'F', 'P', 'M']:
            logging.error('Error: unsupported attribute display mode.')

        ret = list()
        if attr_mode == 'masked' or attr_mode == 'M':
            if self._data1_attributes_partial[attr_id] is not None:
                ret = ['partial', [self._data1_attributes_partial[attr_id], self._data2_attributes_partial[attr_id]]]
            else:
                ret = ['full', [self._data1_attributes_full[attr_id], self._data2_attributes_full[attr_id]]]
        elif attr_mode == 'partial' or attr_mode == 'P':
            ret = ['full', [self._data1_attributes_full[attr_id], self._data2_attributes_full[attr_id]]]
        elif attr_mode == 'full' or attr_mode == 'F':
            logging.warning('Warning: there is no next display for full attribute mode.')
            ret = ['full', [self._data1_attributes_full[attr_id], self._data2_attributes_full[attr_id]]]
        return ret


    def get_ids(self):
        id1_list = [str(self._pair_num)+'-1-'+str(i) for i in range(self.num_of_attr)]
        id2_list = [str(self._pair_num)+'-2-'+str(i) for i in range(self.num_of_attr)]
        return [id1_list, id2_list]


    def get_pair_num(self):
        return self._pair_num


    def _get_character_disclosed_num(self, value):
        character_disclosed_num = 0
        for c in value:
            if c not in ['*', '_', '/']:
                character_disclosed_num += 1
        return character_disclosed_num


    def get_character_disclosed_num(self, row_number, j, display_status):
        """
        get the current character disclosed number for attribute j, at its display status
        input:
            row_number - 1 or 2
            j - attribute j
            display_status - 'M', 'P', or 'F'
        """
        value = ''
        if display_status == 'M':
            return 0
        elif display_status == 'F':
            if row_number == 1:
                value = self._data1_attributes[j]
            else:
                value = self._data2_attributes[j]
        elif display_status == 'P':
            if row_number == 1:
                value = self._data1_helpers[j]
            else:
                value = self._data2_helpers[j]
        else:
            logging.error('Error: unsupported display status.')
            return 0

        return self._get_character_disclosed_num(value)


    def get_total_characters(self, row_number):
        """
        get the total character number of the row number
        """
        total = 0
        attributes = self._data1_attributes
        if row_number == 2:
            attributes = self._data2_attributes
        for value in attributes:
            total += self._get_character_disclosed_num(value)
        return total


    def get_data_raw(self, row_number, col):
        if row_number == 1:
            data = self._data1_raw
        else:
            data = self._data2_raw
        if col < 0 or col >= len(data):
            logging.error('Error: index out of range.')
            return ''
        return data[col]


    def grade(self, answer):
        """
        grade the answer, where the answer is:
        1, 2, 3: different
        4, 5, 6: same
        """
        truth = self._data1_raw[17].rstrip('\n')
        if truth == '0' and answer <= 3:
            return True
        if truth == '1' and answer > 3:
            return True
        return False


class DataPairList(object):
    """
    a list of DataPair, this object only hold DataPair object
    TODO: in get_something function, add the paging function
    """
    def __init__(self, data_pairs=[], indices=None):
        """
        input: raw list of data pairs, for example:
        [
            ['1','','206','NELSON','MITCHELL','1459','03/13/1975','M','B','','******','********___','03/13/1975','*','*','34','6','0'],
            ['1','1000142704, '174','NELSON','MITCHELL SR','1314','07/03/1949','M','B','1000142704','******','******** SR','07/03/1949','*','*','34','6','0']
        ]
        """
        if len(data_pairs)%2 != 0:
            logging.error('Error: dataset not in pair.')

        if indices is not None:
            new_data_pairs = list()
            for row in data_pairs:
                if int(row[0]) in indices:
                    new_data_pairs.append(row)
            data_pairs = new_data_pairs

        self._data_raw = data_pairs
        self._data = list()
        self._id_hash = dict()
        for i in range(0, len(data_pairs), 2):
            if data_pairs[i][0] != data_pairs[i+1][0]:
                logging.error('Error: inconsistent pair number.')
            self._data.append(DataPair(data_pairs[i], data_pairs[i+1]))
            pair_num = int(data_pairs[i][0])
            location = i/2
            self._id_hash[pair_num] = int(location)
        self.idx = 0

        self._size = len(self._data)
        self._kapr_size = self._size


    def __iter__(self):
        return self


    def __next__(self):
        self.idx += 1
        try:
            return self._data[self.idx-1]
        except IndexError:
            self.idx = 0
            raise StopIteration  # Done iterating.


    next = __next__


    def append_data_pair(self, dp):
        """
        input:
            dp - data pair:
            [
                ['1','','206','NELSON','MITCHELL','1459','03/13/1975','M','B','','******','********___','03/13/1975','*','*','34','6','0'],
                ['1','1000142704, '174','NELSON','MITCHELL SR','1314','07/03/1949','M','B','1000142704','******','******** SR','07/03/1949','*','*','34','6','0']
            ]
        """
        if len(dp) != 2:
            logging.error('Error: incorrect data pair.')
        if dp[0][0] != dp[1][0]:
            logging.error('Error: inconsistent pair number.')

        pair_num = int(dp[0][0])
        location = len(self._data)
        self._data.append(DataPair(dp[0], dp[1]))
        self._id_hash[pair_num] = int(location)

        self._size += 1


    def get_data_pair(self, pair_num):
        if pair_num not in self._id_hash:
            return None
        return self._data[self._id_hash[pair_num]]


    def get_data_pair_by_index(self, index):
        if index < 0 or index >= len(self._data):
            logging.error('Error: index out of range')
            return None
        return self._data[index]


    def get_data_display(self, data_mode, data_mode_list=[], left=None, right=None):
        """
        get the html of the current dataset
        input:
            data_mode - display mode, could be 'base', 'full', 'masked', 'minimum', 'moderate', see data_display.py:format_data
            data_mode_list: a list of data mode (to support coming back from working page.)
        output example:
        [
            ['1', '<img src="../static/images/site/missing.png" alt="missing" class="missing_icon">', '<img src="../static/images/site/infinity.png" alt="infinity" class="freq_icon">', 'NELSON', 'MITCHELL', '<img src="../static/images/site/infinity.png" alt="infinity" class="freq_icon">', '03/13/1975','M','B'],
            ['1', '1000142704', '<img src="../static/images/site/infinity.png" alt="infinity" class="freq_icon">', 'NELSON', 'MITCHELL <span style="color:green">SR</span>', '<img src="../static/images/site/infinity.png" alt="infinity" class="freq_icon">', '07/03/1949','M','B']
        ]
        """
        if not left:
            left = 0
        if not right:
            right = len(self._data)
        ret = list()
        if not data_mode_list:
            for d in self._data[left:right]:
                display = d.get_data_display(data_mode)
                ret.append(display[0])
                ret.append(display[1])
        else:
            i = 0
            for d in self._data[left:right]:
                # use this data structure, to get the ffreq data
                display = d.get_data_display(data_mode)
                display_idx = [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]

                attribute_modes = data_mode_list[i]
                i += 1
                j = 0
                display1 = list()
                display2 = list()
                for att_mode in attribute_modes:
                    a_display = d.get_attribute_display(j, att_mode)
                    idx = display_idx[j]
                    display[0][idx] = a_display[0]
                    display[1][idx] = a_display[1]
                    j += 1
                ret.append(display[0])
                ret.append(display[1])
        return ret


    def get_icons(self, indices=None):
        if indices is None:
            return [d.get_icons() for d in self._data]
        ret = list()
        for d in self._data:
            if d.get_pair_num() in indices:
                ret.append(d.get_icons)


    def get_ids(self):
        ret = list()
        for d in self._data:
            id = d.get_ids()
            ret.append(id[0])
            ret.append(id[1])
        return ret


    def get_raw_data(self):
        return self._data_raw

    def get_size(self):
        return self._size

    def size(self):
        return self._size

    def get_kapr_size(self):
        return self._kapr_size

    def set_kapr_size(self, size=NUM_ATTR):
        self._kapr_size = size


def display_matching(attr1, attr2, mode):
    if mode == 'F' or mode == 'full':
        return attr1 == attr2
    if len(attr1) != len(attr2):
        return False
    for i in range(len(attr1)):
        if attr1[i] == '*' or attr2[i] == '*':
            continue
        if attr1[i] != attr2[i]:
            return False
    return True


def get_KAPR_for_dp(dataset, data_pair, display_status, M):
    """
    return the K-Anonymity based Privacy Risk for a data pair at its current display status.
    Input:
        dataset - the whole dataset
        data_pair - DataPair object
        display_status - display status is a list of status, for example:
                         ['M', 'M', 'M', 'M', 'M', 'M'] is all masked display status.
        M - Number of rows that need to be manually linked
    """
    # calculating P
    character_disclosed_num1 = 0
    character_disclosed_num2 = 0
    for j in range(NUM_ATTR):
        character_disclosed_num1 += data_pair.get_character_disclosed_num(1, j, display_status[j])
        character_disclosed_num2 += data_pair.get_character_disclosed_num(2, j, display_status[j])

    total_characters1 = data_pair.get_total_characters(1)
    total_characters2 = data_pair.get_total_characters(2)

    P1 = 1.0*character_disclosed_num1 / total_characters1
    P2 = 1.0*character_disclosed_num2 / total_characters2

    # calculating K
    col_list_F = [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]
    col_list_P = [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    K1 = 0
    K2 = 0
    for i in range(len(dataset)):
        match_flag = True
        for j in range(NUM_ATTR):
            if display_status[j] == 'F':
                col = col_list_F[j]
            elif display_status[j] == 'P':
                col = col_list_P[j]
            else:
                continue
            # TODO: change this to regex matching
            #if dataset[i][col] != data_pair.get_data_raw(1, col):
            if display_matching(dataset[i][col], data_pair.get_data_raw(1, col), display_status[j]) == False:
                match_flag = False
                break
        if match_flag:
            K1 += 1

    for i in range(len(dataset)):
        match_flag = True
        for j in range(NUM_ATTR):
            if display_status[j] == 'F':
                col = col_list_F[j]
            elif display_status[j] == 'P':
                col = col_list_P[j]
            else:
                continue
            if dataset[i][col] != data_pair.get_data_raw(2, col):
                match_flag = False
                break
        if match_flag:
            K2 += 1

    if M == 0:
        logging.error('Empty dataset to calculate kapr.')
    if K1 == 0:
        logging.error('Cannot find data in full dataset.')
        K1 = 1
    if K2 == 0:
        logging.error('Cannot find data in full dataset.')
        K2 = 1
    # if everything is opened for a data, the K-anonymity should be 1
    if display_status.count('F') == NUM_ATTR:
        K1 = 1
        K2 = 1
    
    KAPR1 = (1.0/M)*(1.0/K1)*P1
    KAPR2 = (1.0/M)*(1.0/K2)*P2
    KAPR = KAPR1 + KAPR2

    return KAPR


def KAPR_delta(DATASET, data_pair, display_status, M):
    """
    for the current display status, get all possible next KAPR delta.

    Note: cannot use next_KAPR - KAPR == 0 to decide if an attribute has partial mode or not. Why?
          because the k is different, if the attribute mode is P, then it will use the helper to 
          calculate k (inherently use the length of the string), and the k is different.
    M - Number of rows that need to be manually linked
    """
    delta = list()
    current_KAPR = get_KAPR_for_dp(DATASET, data_pair, display_status, M)
    for i in range(NUM_ATTR):
        state = display_status[i]
        next_display = data_pair.get_next_display(i, state)
        if next_display[0] == 'full':
            display_status[i] = 'F'
        elif next_display[0] == 'partial':
            display_status[i] = 'P'
        else:
            logging.error('Error: wrong attribute display mode returned.')
        next_KAPR = get_KAPR_for_dp(DATASET, data_pair, display_status, M)
        id = data_pair.get_ids()[0][i]
        delta.append((id, 100.0*next_KAPR - 100.0*current_KAPR))
        display_status[i] = state
    return delta


def open_cell(user_key, full_data, working_data, pair_num, attr_num, mode, r, kapr_limit=100):
    """
    openning a clickable cell, full_data is the full database, working_data is the data that need to manually linked.
    pair_num and attr_num are string
    r is redis handler
    return a dict with following keys:
    value1, value2, mode, KAPR, result, new_delta
    """
    ret = dict()

    pair_id = int(pair_num)
    attr_id = int(attr_num)

    pair = working_data.get_data_pair(pair_id)
    attr = pair.get_attributes(attr_id)
    attr1 = attr[0]
    attr2 = attr[1]
    helper = pair.get_helpers(attr_id)
    helper1 = helper[0]
    helper2 = helper[1]

    attr_display_next = pair.get_next_display(attr_id = attr_id, attr_mode = mode)
    
    # TODO: assert the mode is consistent with the display_mode in redis

    """ no character disclosed percentage now
    for character disclosure percentage, see branch ELSI
    """

    # get K-Anonymity based Privacy Risk
    old_display_status1 = list()
    old_display_status2 = list()
    key1_prefix = user_key + '-' + pair_num + '-1-'
    key2_prefix = user_key + '-' + pair_num + '-2-'
    for attr_i in range(NUM_ATTR):
        old_display_status1.append(r.get(key1_prefix + str(attr_i)))
        old_display_status2.append(r.get(key2_prefix + str(attr_i)))
    new_display_status = copy.deepcopy(old_display_status1)
    new_display_status[attr_id] = 'F' if attr_display_next[0] == 'full' else 'P'

    old_KAPR = get_KAPR_for_dp(full_data, pair, old_display_status1, 2*working_data.get_kapr_size())
    KAPR = get_KAPR_for_dp(full_data, pair, new_display_status, 2*working_data.get_kapr_size())
    KAPRINC = KAPR - old_KAPR
    KAPR_key = user_key + '_KAPR'
    overall_KAPR = 100*(float(r.get(KAPR_key)) + KAPRINC)
    if overall_KAPR > kapr_limit:
        ret['result'] = 'fail'
        ret['KAPR'] = 0
        return ret

    # success! update the display status in redis, update KAPR, get delta for KAPR
    ret['value1'] = attr_display_next[1][0]
    ret['value2'] = attr_display_next[1][1]
    ret['mode'] = attr_display_next[0]

    key1 = user_key + '-' + pair_num + '-1-' + attr_num
    key2 = user_key + '-' + pair_num + '-2-' + attr_num
    r.set(key1, new_display_status[attr_id])
    r.set(key2, new_display_status[attr_id])
    r.incrbyfloat(KAPR_key, KAPRINC)
    ret['id'] = pair_num + '-1-' + attr_num
    ret['KAPR'] = overall_KAPR
    ret['result'] = 'success'

    # refresh the delta of KAPR
    new_delta_list = KAPR_delta(full_data, pair, new_display_status, 2*working_data.get_kapr_size())
    ret['new_delta'] = new_delta_list

    return ret


def batched_open_cell(user_key, full_data, working_data, ids, data_mode_list, r, kapr_limit=100):
    size = len(ids)
    for i in range(size):
        for j in range(NUM_ATTR):
            id1 = ids[i][0][j]
            pair_num = str(id1.split('-')[0])
            attr_num = str(id1.split('-')[2])
            data_mode = data_mode_list[i][j]

            if data_mode == 'partial' or data_mode == 'P':
                open_cell(user_key, full_data, working_data, pair_num, attr_num, 'masked', r, kapr_limit)
            elif data_mode == 'full' or data_mode == 'F':
                open_cell(user_key, full_data, working_data, pair_num, attr_num, 'masked', r, kapr_limit)
                open_cell(user_key, full_data, working_data, pair_num, attr_num, 'partial', r, kapr_limit)


def get_kaprlimit(full_data, working_data, data_mode):
    KAPR = 0.0
    for dp in working_data:
        display_status = list()
        if data_mode == 'minimum':
            for i in range(NUM_ATTR):
                if dd.DATA_MODE_MINIMUM[i] == 'partial':
                    if dp.has_partial_mode(i):
                        display_status.append('P')
                    else:
                        display_status.append('M')
                else:
                    display_status.append(dd.DATA_MODE_MINIMUM[i][0].upper())
        elif data_mode == 'moderate':
            for i in range(NUM_ATTR):
                if i == 0:
                    if dd.DATA_MODE_MINIMUM[i] == 'partial':
                        if dp.has_partial_mode(i):
                            display_status.append('P')
                        else:
                            display_status.append('M')
                    else:
                        display_status.append(dd.DATA_MODE_MINIMUM[i][0].upper())
                elif i == 4:
                    display_status.append('F')
                elif i == 5:
                    display_status.append('M')
                else:
                    if dp.attribute_match(i):
                        display_status.append('M')
                    else:
                        display_status.append('F')
        else:
            logging.error('unsupported data mode in get_kaprlimit().')
        KAPR += get_KAPR_for_dp(full_data, dp, display_status, 2*working_data.size())

    return 100.0*KAPR
