class Runner

	def self.run(program, argument_string = nil, &block)
		self.new(program, argument_string).run(&block)
	end

	def initialize(program, argument_string)
		@program, @argument_string = program, argument_string
	end

	def run(&block)
		output = []

		process = IO.popen(@argument_string ? [@program, @argument_string] : @program, :err => [:child, :out]) do |io|
			io.each_line do |l|
				output << l.chomp
				block.call(l)
			end
		end

		raise RuntimeError, "Program exited with a non-zero status code (#{$?})", output if $? != 0

		output
	end

end
