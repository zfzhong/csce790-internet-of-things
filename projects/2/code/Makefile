compare: hmm
	python3 compare_result.py robot_perception_test.dat predicted.dat

em:
	python3 gen_emit_matrix.py grid.dat robot_perception_train.dat > em.dat

tm:
	python3 gen_trans_matrix.py grid.dat robot_perception_train.dat > tm.dat

hmm: em tm
	python3 hmm_viterbi_test.py 17 init_prob.dat tm.dat em.dat robot_perception_test.dat > predicted.dat

clean:
	rm em.dat tm.dat predicted.dat 