compare: hmm
	python3 compare_result.py robot_perception_test.dat predicted.dat

em:
	python3 gen_matrix.py robot_perception_train.dat E 0.05 > em.dat

tm:
	python3 gen_matrix.py robot_perception_train.dat T 0.05 > tm.dat

hmm: em tm
	python3 hmm_viterbi.py tm.dat em.dat robot_perception_test.dat > predicted.dat

clean:
	rm em.dat tm.dat predicted.dat 