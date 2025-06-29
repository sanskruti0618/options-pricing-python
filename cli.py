import argparse
from options_pricing.models.black_scholes import black_scholes
from options_pricing.models.binomial import binomial_tree

def main():
    parser = argparse.ArgumentParser(description="Options Pricing CLI Tool")

    parser.add_argument('--model', choices=['black-scholes', 'binomial'], required=True, help="Pricing model to use")
    parser.add_argument('--option', choices=['call', 'put'], required=True, help="Option type")
    parser.add_argument('--S', type=float, required=True, help="Spot price")
    parser.add_argument('--K', type=float, required=True, help="Strike price")
    parser.add_argument('--T', type=float, required=True, help="Time to maturity (years)")
    parser.add_argument('--r', type=float, required=True, help="Risk-free rate")
    parser.add_argument('--sigma', type=float, required=True, help="Volatility")
    parser.add_argument('--N', type=int, help="Steps for Binomial model (default=100)")
    parser.add_argument('--american', action='store_true', help="Use American option for binomial")

    args = parser.parse_args()

    if args.model == 'black-scholes':
        price = black_scholes(args.S, args.K, args.T, args.r, args.sigma, option_type=args.option)
    elif args.model == 'binomial':
        N = args.N if args.N else 100
        price = binomial_tree(args.S, args.K, args.T, args.r, args.sigma, N=N, option_type=args.option, american=args.american)

    print(f"{args.model.title()} {args.option.title()} Option Price: {price:.4f}")

if __name__ == "__main__":
    main()
