
# Read the robot training file

# knowledge of environment
num_locations = 16 # 4x4 grid, some grids are not allowed
num_colors = 4
color_strings = ['r', 'g', 'b', 'y']

train_file = "robot_perception_train.dat"

num_data_sequence = 200

# read the training data
fid = open(train_file, 'r')
Lines = fid.readlines()

# parse the train sequence
# colors are assigned index 1, 2, 3, 4 for easy HMM matrix building
x_coord = []
y_coord = []
color = []
for line in Lines:
    string_info = line.split(' ')
    coord_val_string = string_info[0]
    color_val_string = string_info[1]

    # add the color info
    color.append(color_strings.index(color_val_string[0]) + 1)

    # add the coordinate info
    coord_val_string = coord_val_string.split(':')

    x_coord.append(int(coord_val_string[0]))
    y_coord.append(int(coord_val_string[1]))

