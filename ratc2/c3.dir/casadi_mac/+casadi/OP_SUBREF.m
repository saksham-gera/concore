function v = OP_SUBREF()
  persistent vInitialized;
  if isempty(vInitialized)
    vInitialized = casadiMEX(0, 76);
  end
  v = vInitialized;
end
