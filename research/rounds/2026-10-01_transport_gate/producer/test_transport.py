import unittest
import numpy as np
from transport import Network, S, C, Q, D, AMPLITUDE, BIAS, rk4


class TransportControls(unittest.TestCase):
    def setUp(self):
        self.net = Network(S, C, np.ones(3))

    def close(self, actual, expected, atol=2e-12):
        np.testing.assert_allclose(actual, expected, rtol=0, atol=atol)

    def test_conserved_null_space_and_shutdown(self):
        q = self.net.charges()
        self.assertEqual(q.shape, (3, 1))
        self.close(S.T @ q, np.zeros((3, 1)))
        self.close(self.net.A @ self.net.C_half @ q, np.zeros((3, 1)))
        stopped = Network(S, C, np.zeros(3))
        self.assertEqual(stopped.charges().shape[1], 3)
        self.close(stopped.propagate(np.array([.02, -.01, .01]), BIAS, 20), [.02,-.01,.01])

    def test_compatible_stationary_state_is_rate_independent(self):
        expected = AMPLITUDE * np.array([5/6,-1/3,-1/2])
        for rates in [np.ones(3), np.array([1.,2.,4.])]:
            net = Network(S, C, rates)
            self.assertTrue(net.compatibility(BIAS)['compatible'])
            state = net.stationary(BIAS)
            self.close(state, expected)
            self.close(net.progress(state, BIAS), np.zeros(3))

    def test_conserved_operator_is_invisible(self):
        self.close(S.T @ Q, np.zeros(3))
        self.close(S.T @ (D + 5*Q), S.T @ D)
        self.close(self.net.propagate(np.zeros(3), S.T @ Q*AMPLITUDE, 10), np.zeros(3))

    def test_incompatible_cycle_and_rate_dependence(self):
        bias = AMPLITUDE * np.ones(3)
        self.assertFalse(self.net.compatibility(bias)['compatible'])
        self.close(self.net.stationary(bias), np.zeros(3))
        self.close(self.net.progress(np.zeros(3), bias), bias)
        uneven = Network(S,C,np.array([1.,2.,4.]))
        state = uneven.stationary(bias)
        self.close(state, AMPLITUDE*np.array([11/21,-8/21,-1/7]))
        self.close(uneven.progress(state,bias), np.full(3,12*AMPLITUDE/7))
        self.close(uneven.derivative(state,bias), np.zeros(3))

    def test_signed_cancellation_and_reversal(self):
        zero = np.zeros(3)
        first = self.net.propagate(zero, BIAS, 1)
        result = self.net.propagate(first, -BIAS, 1)
        equilibrium = self.net.stationary(BIAS)
        e = np.column_stack([self.net.propagate(np.eye(3)[:,i], zero, 1) for i in range(3)])
        self.close(result, -(np.eye(3)-e) @ (np.eye(3)-e) @ equilibrium)
        self.assertGreater(np.linalg.norm(result), 1e-4)
        reverse = self.net.propagate(self.net.propagate(zero, -BIAS, 1), BIAS, 1)
        self.close(reverse, -result)
        self.close(Q @ result, 0)

    def test_washout_and_nonzero_initial_charge(self):
        result = self.net.propagate(self.net.propagate(np.zeros(3), BIAS, 1),-BIAS,1)
        washed = self.net.propagate(result, np.zeros(3), 20)
        self.assertLess(np.linalg.norm(washed),1e-10)
        initial = np.array([.01,.02,.03])
        final = self.net.propagate(initial, BIAS, 2)
        self.close(Q @ final,Q @ initial)

    def test_free_energy_and_nondiagonal_susceptibility(self):
        chi = np.array([[1.,.1,0.],[.1,2.,.2],[0.,.2,3.]])
        net = Network(S,chi,np.array([1.,2.,4.]))
        initial = np.array([.02,-.01,-.01])
        states = [net.propagate(initial,np.zeros(3),float(t)) for t in np.linspace(0,3,31)]
        energy = [float(x @ net.C_inv @ x / 2) for x in states]
        self.assertTrue(np.all(np.diff(energy) <= 1e-15))
        self.close(net.A @ net.C_half @ Q,np.zeros(3))
        self.close(Q @ states[-1],Q @ initial)

    def test_independent_integration_converges(self):
        exact = self.net.propagate(self.net.propagate(np.zeros(3),BIAS,1),-BIAS,1)
        errors = []
        for steps in [32,64,128]:
            approx = rk4(self.net,rk4(self.net,np.zeros(3),BIAS,1,steps),-BIAS,1,steps)
            errors.append(np.linalg.norm(approx-exact))
        self.assertTrue(all(a>b for a,b in zip(errors,errors[1:])))
        self.assertLess(errors[-1],2e-10)

    def test_invalid_inputs_rejected(self):
        for chi,rates in [(np.diag([1,2,0]),np.ones(3)),
                          (np.eye(3),np.array([1,-1,1]))]:
            with self.assertRaises(ValueError):
                Network(S,chi,rates)


if __name__ == '__main__':
    unittest.main()
